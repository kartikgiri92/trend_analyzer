import re
import tweepy

import prime.models as prime_models
import config.settings as config_settings

from prime.woeid_list import India
from random import shuffle
from django.db import IntegrityError
from django.db import connection, reset_queries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# To Check Number of Query Execution
# print(len(connection.queries))
# reset_queries()

# Info
# trends_fetch_quantity always [1, 50]
# tweets_fetch_quantity always [1, 100]
top_trending_quantity = 10  # Top Trending should always be <= Trends Fetch Quantity
trends_fetch_quantity = 30  # Top Trending should always be <= Trends Fetch Quantity
tweets_fetch_quantity = 80

analyser = SentimentIntensityAnalyzer()

def sentiment_classify(compound_value):
    if(compound_value > 0.5):
        # Positive
        return(1, 0, 0)
    if(compound_value < -0.5):
        # Negative
        return(0, 0, 1)
    else:
        # Neutral
        return(0, 1, 0)


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return(input_txt)

def data_preprocessing(input_txt):
    # remove twitter Return handles (RT @xxx:)
    input_txt = remove_pattern(input_txt, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    input_txt = remove_pattern(input_txt, "@[\w]*")
    # remove URL links (httpxxx)
    input_txt = remove_pattern(input_txt, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    input_txt = str.replace(input_txt, "[^a-zA-Z#]", " ")
    
    return(input_txt)

def prime_func(request):  # Return Dict object
    if(config_settings.DEBUG):
        reset_queries() # To know number of Queries
    
    # Authenticating API keys
    try:
        auth = tweepy.AppAuthHandler(config_settings.api_key, config_settings.api_secret_key)
        api = tweepy.API(auth)
    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'During keys Auth')
        return({'message' : 'Error while Authenticating keys', 'status' : False})

    # Fetch current Trends
    try:
        # List containing trends as dict objects
        # The api always fetch 50 trends
        current_trends_list = api.trends_place(id = India)[0]['trends']
        length_of_current_trends = len(current_trends_list)

    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'Error While Fetching Trends')
        return({'message' : 'Error While Fetching Trends', 'status' : False})

    if((length_of_current_trends < top_trending_quantity) or (length_of_current_trends < trends_fetch_quantity)
            or (top_trending_quantity > trends_fetch_quantity)):
        prime_models.Log.objects.create(message = 'Length of Current Trends less than Needed Quantity')
        return({'message' : 'Length of Current Trends less than Needed Quantity', 'status' : False})
    else:
        shuffle(current_trends_list)
        current_trends_list = current_trends_list[0: trends_fetch_quantity]
        length_of_current_trends = len(current_trends_list)

    for i in range(length_of_current_trends):
        if(current_trends_list[i]['name'][0] == '#'):   current_trends_list[i]['name'] = current_trends_list[i]['name'][1:]
        try:
            trend_obj, created = prime_models.Trend.objects.get_or_create(name = current_trends_list[i]['name'],
                    url = current_trends_list[i]['url'], query = current_trends_list[i]['query'])
        except IntegrityError:
            prime_models.Log.objects.create(message = 'Unique Constraint Failed for Unique Trend Name for trend {}'.\
                format(current_trends_list[i]['name']))
            continue

        try :
            current_tweets_list = api.search(q = trend_obj.query,
                result_type = 'popular', count = tweets_fetch_quantity, 
                include_entities = False, lang = 'en', tweet_mode = 'extended')
            if(len(current_tweets_list) < (tweets_fetch_quantity//2)):
                current_tweets_list = api.search(q = trend_obj.query, 
                    result_type = 'mixed', count = tweets_fetch_quantity, 
                    include_entities = False, lang = 'en', tweet_mode = 'extended')
            if(len(current_tweets_list) == 0):
                prime_models.Log.objects.create(message = 'Zero Tweets Fetched for trend {}'.format(trend_obj.name))
                continue
        except tweepy.TweepError:
            prime_models.Log.objects.create(message = 'Error While Fetching Tweets for trend {}'.format(trend_obj.name))
            continue

        new_tweets_obj_list = []
        id_str_list = [tmp_tweet.id_str for tmp_tweet in current_tweets_list]
        existing_tweets_index = 0
        existing_tweets = list(prime_models.Tweet.objects.filter(trend = trend_obj, id_str__in = id_str_list))

        for tmp_tweet in current_tweets_list:
            # Tweet obj already Exist
            if((len(existing_tweets) > existing_tweets_index) and \
                (tmp_tweet.id_str == existing_tweets[existing_tweets_index].id_str)):
                existing_tweets[existing_tweets_index].retweet_count = tmp_tweet.retweet_count
                existing_tweets[existing_tweets_index].favourite_count = tmp_tweet.favorite_count
                existing_tweets[existing_tweets_index].save()
                existing_tweets_index += 1
            else:
                # New Tweet obj will be created
                tweet_txt = data_preprocessing(tmp_tweet.full_text)
                cmpd_value = analyser.polarity_scores(tweet_txt)['compound']
                try:
                    oem_html = api.get_oembed(id = tmp_tweet.id_str, omit_script = True)['html']
                except tweepy.TweepError:
                    # prime_models.Log.objects.create(message = 'OEM NOT GENERATED for tweet {}'.format(tmp_tweet.id_str))
                    continue
                tweet_obj = prime_models.Tweet(text = tweet_txt, trend = trend_obj,
                        id_str = tmp_tweet.id_str, retweet_count = tmp_tweet.retweet_count,
                        favourite_count = tmp_tweet.favorite_count,
                        oembed_html = oem_html, compound_value = cmpd_value)
                tmp_pst, tmp_neut, tmp_neg = sentiment_classify(cmpd_value)
                trend_obj.num_positive += tmp_pst
                trend_obj.num_neutral += tmp_neut
                trend_obj.num_negative += tmp_neg
                new_tweets_obj_list.append(tweet_obj)
        try:
            prime_models.Tweet.objects.bulk_create(new_tweets_obj_list)
        except IntegrityError:
            prime_models.Log.objects.create(message = 'Unique Constraint Failed for Unique Tweet Id for trend {}'.format(trend_obj.name))

        if(current_trends_list[i]['tweet_volume']):
            trend_obj.total_tweet_volume = current_trends_list[i]['tweet_volume']
             
        try:
            if(trend_obj.name[0] == '#'):
                trend_obj.name = trend_obj.name[1:]
            trend_obj.save()
        except IntegrityError:
            prime_models.Log.objects.create(message = 'Unique Constraint Failed for Unique Trend Name for trend {}'.\
                format(current_trends_list[i]['name']))
            trend_obj.delete()

    # Delete Trends With No Tweets
    del_trends = list(prime_models.Trend.objects.all().prefetch_related('tweet_set'))
    for tmp_obj in del_trends:
        if(not(len(tmp_obj.tweet_set.all()))):
            tmp_obj.delete()

    #  Mark Last Updated as Trending
    all_trends = list(prime_models.Trend.objects.all().order_by('-last_updated'))
    var_index = min(len(all_trends), top_trending_quantity)
    for i in range(0, var_index):
        all_trends[i].is_top_trending = True
        all_trends[i].save()
    # Mark Rest as Not Trending
    for i in range(var_index, len(all_trends)):
        if(all_trends[i].is_top_trending):
            all_trends[i].is_top_trending = False
            all_trends[i].save()

    if(config_settings.DEBUG):
        print(len(connection.queries)) # To know number of Queries
        reset_queries()
    return({'message' : 'Successfull data fetching, cleaning and updating', 'status' : True})
