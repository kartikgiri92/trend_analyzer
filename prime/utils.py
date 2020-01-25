import tweepy

import prime.models as prime_models
import config.settings as config_settings

from prime.woeid_list import India
from django.db import connection, reset_queries

# To Check Number of Query Execution
# print(len(connection.queries))
# reset_queries()

# Alter this value to make change in number of Top Trending Trends
top_trending_quantity = 10 

def select_top_trending(current_trends_list, top_trending_quantity):


    return([])

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
    except tweepy.TweepError:
        prime_models.Log.objects.create(message = 'Error While Fetching Trends')
        return({'message' : 'Error While Fetching Trends', 'status' : False})

    top_trending_list = select_top_trending(current_trends_list, top_trending_quantity)

    


    return({'message' : 'Successfull data fetching, cleaning and updating', 'status' : True})
