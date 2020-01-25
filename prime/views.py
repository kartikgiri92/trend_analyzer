import prime.models as prime_models
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

