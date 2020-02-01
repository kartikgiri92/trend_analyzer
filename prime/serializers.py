import time
import prime.models as prime_models
import prime.utils as prime_utils
from rest_framework import serializers

class BaseTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = prime_models.Tweet
        fields = ('id_str', 'text', 'retweet_count', 'favourite_count', 'compound_value')

class BaseTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = prime_models.Trend
        fields = ('id', 'url', 'name', 'total_tweet_volume', 'last_updated', 
        	'num_positive', 'num_negative', 'num_neutral', 'is_top_trending')

# class TrendWithTweetSerializer(serializers.ModelSerializer):

#     tweet_set = BaseTweetSerializer(many=True)

#     class Meta:
#         model = prime_models.Trend
#         fields = ('id', 'url', 'name', 'total_tweet_volume', 'last_updated', 'tweet_set')