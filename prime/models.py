from django.db import models

# Create your models here.
class Trend(models.Model):
    url = models.TextField()
    name = models.TextField(unique = True)
    query = models.TextField()
    positive_percentage = models.IntegerField(default = 0)
    neutral_percentage = models.IntegerField(default = 0)
    negative_percentage = models.IntegerField(default = 0)
    total_tweet_volume = models.TextField(default = '0')
    is_top_trending = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return(self.name)

class Tweet(models.Model):
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    tweet_id = models.TextField()
    text = models.TextField()
    retweet_count = models.TextField()
    favourite_count = models.TextField()
    oembed_html = models.TextField()
    compound_value = models.IntegerField(default = 0)
    
    def __str__(self):
        return(self.text)

class Log(models.Model):
    last_updated = models.DateTimeField(auto_now = True)
    message = models.TextField()
    solved = models.BooleanField(default = False)
    
    def __str__(self):
        return(self.message)
