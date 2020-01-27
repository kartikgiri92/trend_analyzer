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