from django.db import models

# Create your models here.
class Trend(models.Model):
    url = models.CharField(max_length = 50)
    name = models.CharField(unique = True, max_length = 125)
    query = models.CharField(max_length = 50)
    num_positive = models.IntegerField(default = 0)
    num_neutral = models.IntegerField(default = 0)
    num_negative = models.IntegerField(default = 0)
    total_tweet_volume = models.CharField(default = '0', max_length = 20)
    is_top_trending = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return(self.name)

class Tweet(models.Model):
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    id_str = models.CharField(unique = True, max_length=20)
    text = models.CharField(max_length = 300)
    retweet_count = models.CharField(max_length = 20)
    favourite_count = models.CharField(max_length = 20)
    compound_value = models.FloatField(default = 0)
    
    def __str__(self):
        return(self.text)

class Log(models.Model):
    last_updated = models.DateTimeField(auto_now = True)
    message = models.CharField(max_length = 250)
    solved = models.BooleanField(default = False)
    
    def __str__(self):
        return(self.message)
