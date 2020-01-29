import prime.models as prime_models
import prime.utils as prime_utils
import prime.serializers as prime_serializers

import time
from rest_framework.parsers import FileUploadParser
from django.db import connection, reset_queries
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (ListAPIView, 
    CreateAPIView, UpdateAPIView, RetrieveAPIView, ListCreateAPIView,
    RetrieveUpdateAPIView, GenericAPIView
)

# To Check Number of Query Execution #
# print(len(connection.queries))
# reset_queries()

class foung(GenericAPIView):
    # This API is called only through CRON
    def get(self, request, *args, **kwargs):
        return Response(prime_utils.prime_func(request))

class GetTrend(ListAPIView, RetrieveAPIView):
    lookup_field = 'id'
    queryset = prime_models.Trend.objects.all().order_by('-last_updated')
    serializer_class = prime_serializers.BaseTrendSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = prime_models.Trend.objects.filter(id=kwargs['data'])
        if(not(instance)):
            return Response({'message':'Trend does not exist', 'status':False})
        else:
            instance = instance[0]
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_available_tweets = instance.num_positive + instance.num_neutral + instance.num_negative

        try:
            data['positive_percentage'] = 100 * (instance.num_positive/total_available_tweets)
            data['neutral_percentage'] = 100 * (instance.num_neutral/total_available_tweets)
            data['negative_percentage'] = 100 * (instance.num_negative/total_available_tweets)
        except ZeroDivisionError:
            data['positive_percentage'] = 0
            data['neutral_percentage'] = 0
            data['negative_percentage'] = 0

        if(data['positive_percentage'] >= 1):
            temp = list(prime_models.Tweet.objects.filter(trend = instance, compound_value__gt = 0.5).\
                order_by('-favourite_count', '-retweet_count'))
            min_index = min(len(temp), 5)
            data['positive_tweets'] = [temp[i].oembed_html for i in range(0, min_index)]
        if(data['negative_percentage'] >= 1):
            temp = list(prime_models.Tweet.objects.filter(trend = instance, compound_value__lt = -0.5).\
                order_by('-favourite_count', '-retweet_count'))
            min_index = min(len(temp), 5)
            data['negative_tweets'] = [temp[i].oembed_html for i in range(0, min_index)]
        if(data['neutral_percentage'] >= 1):
            temp = list(prime_models.Tweet.objects.filter(trend = instance, compound_value__range = (-0.5, 0.5)).\
                order_by('-favourite_count', '-retweet_count'))
            min_index = min(len(temp), 5)
            data['neutral_tweets'] = [temp[i].oembed_html for i in range(0, min_index)]

        return Response({'data':data,'status':True})

    def list(self, request, *args, **kwargs):
        if(len(kwargs)):
            return(self.retrieve(request, data = kwargs[self.lookup_field]))
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if(serializer.data):
            return Response({'data':serializer.data,'status':True})
        else:
            return Response({'message':"No Trends",'status':False})

class GetActiveTrend(ListAPIView):
    queryset = prime_models.Trend.objects.filter(is_top_trending = True)
    serializer_class = prime_serializers.BaseTrendSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if(serializer.data):
            return Response({'data':serializer.data,'status':True})
        else:
            return Response({'message':"No Active Trends",'status':False})