from django.db import models

# Create your models here.
class Trend(models.Model):
    url = models.TextField()
    name = models.TextField(unique = True)
    query = models.TextField()
    num_positive = models.IntegerField(default = 0)
    num_neutral = models.IntegerField(default = 0)
    num_negative = models.IntegerField(default = 0)
    total_tweet_volume = models.TextField(default = '0')
    is_top_trending = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return(self.name)

class Tweet(models.Model):
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    id_str = models.TextField(unique = True)
    text = models.TextField()
    retweet_count = models.TextField()
    favourite_count = models.TextField()
    oembed_html = models.TextField()
    compound_value = models.FloatField(default = 0)
    
    def __str__(self):
        return(self.text)

class Log(models.Model):
    last_updated = models.DateTimeField(auto_now = True)
    message = models.TextField()
    solved = models.BooleanField(default = False)
    
    def __str__(self):
        return(self.message)
