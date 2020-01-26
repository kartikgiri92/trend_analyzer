import re
import tweepy

import prime.models as prime_models
import config.settings as config_settings

from prime.woeid_list import India

from django.db import connection, reset_queries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# To Check Number of Query Execution
# print(len(connection.queries))
# reset_queries()

# Alter this value to make change in number of Top Trending Trends
top_trending_quantity = 10
analyser = SentimentIntensityAnalyzer()

def select_top_trending(length_of_current_trends, current_trends_list, top_trending_quantity):
    volume_given, volume_not_given = [], []
    return_value = [0 for i in range(length_of_current_trends)]
    temp = {}
    for i in range(0,len(current_trends_list)):
        if(current_trends_list[i]['tweet_volume']):
            volume_given.append(current_trends_list[i])
        else:
            volume_not_given.append(current_trends_list[i])
        temp[current_trends_list[i]['name']] = i

    if(len(volume_given) < top_trending_quantity):
        volume_given += volume_not_given[0 :  top_trending_quantity - len(volume_given)]
    else:
        volume_given = volume_given[0 : top_trending_quantity]

    for i in volume_given:
        return_value[temp[i['name']]] = 1
    return(return_value)

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
    
    # Authenticating API keys
    try:
        auth = tweepy.AppAuthHandler(config_settings.api_key, config_settings.api_secret_key)
        api = tweepy.API(auth)
    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'During keys Auth')
        return({'message' : 'Error while Authenticating keys', 'status' : False})

    # Fetch 50 current Trends
    try:
        # List containing trends as dict objects
        current_trends_list = api.trends_place(id = India)[0]['trends']
        length_of_current_trends = len(current_trends_list)

    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'Error While Fetching Trends')
        return({'message' : 'Error While Fetching Trends', 'status' : False})

    if(length_of_current_trends < top_trending_quantity):
        prime_models.Log.objects.create(message = 'Length of Current Trends less than Needed Quantity')
        return({'message' : 'Length of Current Trends less than Needed Quantity', 'status' : False})

    top_trending_indexes = select_top_trending(length_of_current_trends, current_trends_list, top_trending_quantity)

    prime_models.Trend.objects.filter(is_top_trending = True).update(is_top_trending = False)

    for i in range(length_of_current_trends):
        trend_obj, created = prime_models.Trend.objects.get_or_create(name = current_trends_list[i]['name'],
                    url = current_trends_list[i]['url'], query = current_trends_list[i]['query'])
        tweets_obj_list = []
        if(created):
            try :
                current_tweets_list = api.search(q = trend_obj.query,
                        result_type = 'popular', count = 50, 
                        include_entities = False, lang = 'en')
                if(len(current_tweets_list) < 25):
                    current_tweets_list = api.search(q = trend_obj.query,
                        result_type = 'mixed', count = 50, 
                        include_entities = False, lang = 'en')
            except tweepy.TweepError:
                prime_models.Log.objects.create(message = 'Error While Fetching Tweets for topic {}'.format(trend_obj.name))
                trend_obj.delete()
                continue

            for tmp_tweet in current_tweets_list:
                tweet_txt = data_preprocessing(tmp_tweet.text)
                cmpd_value = analyser.polarity_scores(tweet_txt)['compound']
                try:
                    oem_html = api.get_oembed(id = tmp_tweet.id_str, omit_script = True)['html']
                except tweepy.TweepError:
                    prime_models.Log.objects.create(message = 'OEM NOT GENERATED for tweet {}'.format(tmp_tweet.id_str))
                    continue
                tweet_obj = Tweet(text = tweet_txt, trend = trend_obj,
                        tweet_id = tmp_tweet.id_str, retweet_count = tmp_tweet.retweet_count,
                        favourite_count = tmp_tweet.favorite_count,
                        oembed_html = oem_html, compound_value = cmpd_value)
                tweets_obj_list.append(tweet_obj)

        else:
            a = 2

        break

        # Update Trend Obj Other Fields


    return({'message' : 'Successfull data fetching, cleaning and updating', 'status' : True})
