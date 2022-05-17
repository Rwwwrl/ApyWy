from typing import Union

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from rest_framework.views import APIView

DjangoView = Union[View, APIView]
