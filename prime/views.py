import time
import prime.models as prime_models
import prime.utils as prime_utils
import prime.serializers as prime_serializers
from mysite_config import foung_required_key, get_request_key
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, RetrieveAPIView, GenericAPIView)


# To Check Number of Query Execution #
# print(len(connection.queries))
# reset_queries()

class foung(GenericAPIView):
    # This API is called only through CRON
    def get(self, request, *args, **kwargs):
        start_time_for_process = time.time()
        try:
            if request.headers['Foung-Required-Key'] != foung_required_key:
                return Response({'message': 'Authentication Failed', 'status': False})
        except KeyError:
            return Response({'message': 'Authentication Failed', 'status': False})

        response_message, response_status = prime_utils.prime_func(request)
        print("----- Total time to complete the process -----", time.time() - start_time_for_process)
        return Response({'message': response_message, 'status': response_status})


class GetTrend(ListAPIView, RetrieveAPIView):
    lookup_field = 'id'
    queryset = prime_models.Trend.objects.all().order_by('-last_updated')
    serializer_class = prime_serializers.BaseTrendSerializer
    num_of_tweets_to_send = 5

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = prime_models.Trend.objects.get(id=kwargs['data'])
        except Exception as e:
            return Response({'message': 'Trend does not exist', 'status': False})
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_available_tweets = instance.num_positive + instance.num_neutral + instance.num_negative

        try:
            data['positive_percentage'] = 100 * (instance.num_positive / total_available_tweets)
            data['neutral_percentage'] = 100 * (instance.num_neutral / total_available_tweets)
            data['negative_percentage'] = 100 * (instance.num_negative / total_available_tweets)
        except ZeroDivisionError:
            data['positive_percentage'] = 0
            data['neutral_percentage'] = 0
            data['negative_percentage'] = 0

        temp = list(
            prime_models.Tweet.objects.filter(trend=instance,
                                              compound_value__gt=prime_utils.positivie_threshold).order_by(
                '-favourite_count', '-retweet_count'))
        min_index = min(len(temp), self.num_of_tweets_to_send)
        data['positive_tweets'] = [temp[i].id_str for i in range(0, min_index)]

        temp = list(
            prime_models.Tweet.objects.filter(trend=instance,
                                              compound_value__lt=prime_utils.negative_threshold).order_by(
                '-favourite_count', '-retweet_count'))
        min_index = min(len(temp), self.num_of_tweets_to_send)
        data['negative_tweets'] = [temp[i].id_str for i in range(0, min_index)]

        temp = list(prime_models.Tweet.objects.filter(trend=instance, compound_value__range=(
            prime_utils.negative_threshold, prime_utils.positivie_threshold)).order_by('-favourite_count',
                                                                                       '-retweet_count'))
        min_index = min(len(temp), self.num_of_tweets_to_send)
        data['neutral_tweets'] = [temp[i].id_str for i in range(0, min_index)]

        return Response({'data': data, 'status': True})

    def list(self, request, *args, **kwargs):
        try:
            if request.headers['Get-Request-Key'] != get_request_key:
                return Response({'message': 'Authentication Failed', 'status': False})
        except KeyError:
            return Response({'message': 'Authentication Failed', 'status': False})

        if len(kwargs):
            return self.retrieve(request, data=kwargs[self.lookup_field])
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response({'data': serializer.data, 'status': True})
        else:
            return Response({'message': "No Trends", 'status': False})


class GetActiveTrend(ListAPIView):
    queryset = prime_models.Trend.objects.filter(is_top_trending=True)
    serializer_class = prime_serializers.BaseTrendSerializer

    def list(self, request, *args, **kwargs):
        try:
            if request.headers['Get-Request-Key'] != get_request_key:
                return Response({'message': 'Authentication Failed', 'status': False})
        except KeyError:
            return Response({'message': 'Authentication Failed', 'status': False})

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response({'data': serializer.data, 'status': True})
        else:
            return Response({'message': "No Active Trends", 'status': False})
