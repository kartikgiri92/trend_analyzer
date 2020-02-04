import re
import tweepy

import prime.models as prime_models
import config.base as config_base

from datetime import datetime, timedelta
from pytz import timezone
from prime.woeid_list import India
from random import shuffle
from django.db import IntegrityError
from django.db import connection, reset_queries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# To Check Number of Query Execution
# print(len(connection.queries))
# reset_queries()

# Info
# tweets_fetch_quantity always in [1, 100]
top_trending_quantity = 20
tweets_fetch_quantity = 75

positivie_threshold = 0.3
negative_threshold = -0.3

analyser = SentimentIntensityAnalyzer()

def deEmojify(inputString):
    return(inputString.encode('ascii', 'ignore').decode('ascii'))

def sentiment_classify(compound_value):
    # return(positive, negative, neutral)
    if(compound_value > positivie_threshold):
        # Positive
        return(1, 0, 0)
    if(compound_value < negative_threshold):
        # Negative
        return(0, 1, 0)
    else:
        # Neutral
        return(0, 0, 1)


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
    # Removing all Emojis
    input_txt = deEmojify(input_txt)
    
    return(input_txt)

def prime_func(request):  # Return Dict object
    
    # Authenticating API keys
    try:
        auth = tweepy.AppAuthHandler(config_base.twitter_key, config_base.twitter_secret_key)
        api = tweepy.API(auth)
    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'During keys Auth')
        return({'message' : 'Error while Authenticating keys', 'status' : False})

    # Fetch current Trends
    try:
        # List containing trends as dict objects
        current_trends_list = api.trends_place(id = India)[0]['trends']
        length_of_current_trends = len(current_trends_list)

    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'Error While Fetching Trends')
        return({'message' : 'Error While Fetching Trends', 'status' : False})

    for i in range(length_of_current_trends):
        current_trends_list[i]['name'] = deEmojify(current_trends_list[i]['name'])
        if(current_trends_list[i]['name'][0] == '#'):
            current_trends_list[i]['name'] = current_trends_list[i]['name'][1:]
        trend_obj, created = prime_models.Trend.objects.get_or_create(name = current_trends_list[i]['name'],
                url = current_trends_list[i]['url'], query = current_trends_list[i]['query'])

        try :
            current_tweets_list = list(api.search(q = trend_obj.query,
                count = tweets_fetch_quantity, lang = 'en', 
                tweet_mode = 'extended'))
            if(len(current_tweets_list) == 0):
                prime_models.Log.objects.create(message = 'Zero Tweets Fetched for trend {}'.format(trend_obj.name))
                continue
        except tweepy.TweepError:
            prime_models.Log.objects.create(message = 'Error While Fetching Tweets for trend {}'.format(trend_obj.name))
            continue

        new_tweets_obj_list = []
        id_str_list = [tmp_tweet.id_str for tmp_tweet in current_tweets_list]
        number_of_positive, number_of_negative, number_of_neutral = 0, 0, 0
        existing_tweets_dic = {}
        existing_tweets = list(prime_models.Tweet.objects.filter(id_str__in = id_str_list))
        for var_xyz in existing_tweets:
            existing_tweets_dic[var_xyz.id_str] = var_xyz

        for tmp_tweet in current_tweets_list:
            # Tweet obj already Exist
            if(tmp_tweet.id_str in existing_tweets_dic):
                existing_tweets_dic[tmp_tweet.id_str].retweet_count = tmp_tweet.retweet_count
                existing_tweets_dic[tmp_tweet.id_str].favourite_count = tmp_tweet.favorite_count
                existing_tweets_dic[tmp_tweet.id_str].save()
            else:
                # New Tweet obj will be created
                tweet_txt = data_preprocessing(tmp_tweet.full_text)
                cmpd_value = analyser.polarity_scores(tweet_txt)['compound']
                tweet_obj = prime_models.Tweet(text = tweet_txt, trend = trend_obj,
                        id_str = tmp_tweet.id_str, retweet_count = tmp_tweet.retweet_count,
                        favourite_count = tmp_tweet.favorite_count,
                        compound_value = cmpd_value)
                tmp_pst, tmp_neg, tmp_neut = sentiment_classify(cmpd_value)
                number_of_positive += tmp_pst
                number_of_negative += tmp_neg
                number_of_neutral += tmp_neut
                new_tweets_obj_list.append(tweet_obj)
        try:
            prime_models.Tweet.objects.bulk_create(new_tweets_obj_list)
            trend_obj.num_positive += number_of_positive
            trend_obj.num_negative += number_of_negative
            trend_obj.num_neutral += number_of_neutral
        except IntegrityError:
            prime_models.Log.objects.create(message = 'Unique Constraint Failed for Unique Tweet Id for trend {}'.format(trend_obj.name))

        if(current_trends_list[i]['tweet_volume']):
            trend_obj.total_tweet_volume = current_trends_list[i]['tweet_volume']
        trend_obj.save();

    # Delete Trends With No Tweets
    del_trends = list(prime_models.Trend.objects.all().prefetch_related('tweet_set'))
    for tmp_obj in del_trends:
        if((len(tmp_obj.tweet_set.all()) == 0) or ((datetime.now(timezone('Asia/Kolkata')) - tmp_obj.last_updated).days > 1)):
            tmp_obj.delete()

    all_trends = list(prime_models.Trend.objects.all().order_by('last_updated', 'num_positive', 'num_negative', 'num_neutral'))
    length_all_trends = len(all_trends)
    var_index = min(length_all_trends, top_trending_quantity)
    # Marking as Not Trending
    for i in range(0, length_all_trends - var_index):
        if(all_trends[i].is_top_trending):
            all_trends[i].is_top_trending = False
            all_trends[i].save()
    # Marking as Trending
    for i in range(length_all_trends - var_index, length_all_trends):
        if(not(all_trends[i].is_top_trending)):
            all_trends[i].is_top_trending = True
            all_trends[i].save()

    return({'message' : 'Successfull data fetching, cleaning and updating', 'status' : True})