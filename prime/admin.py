from django.contrib import admin
import prime.models as prime_models

# Register your models here.

class TrendAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_tweet_volume',
        'num_positive', 'num_neutral', 'num_negative', 
        'is_top_trending', 'last_updated')

class TweetAdmin(admin.ModelAdmin):
    list_display = ('trend', 'id_str',
        'text', 'compound_value')

class LogAdmin(admin.ModelAdmin):
    list_display = ('message', 'solved', 'last_updated')

admin.site.register(prime_models.Trend, TrendAdmin)
admin.site.register(prime_models.Tweet, TweetAdmin)
admin.site.register(prime_models.Log, LogAdmin)