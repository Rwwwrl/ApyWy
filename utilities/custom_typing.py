from typing import TypeVar

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from rest_framework.views import APIView

from ..constants.request import const as req_const
from ..constants.response import const as res_const
from ..constants.const import ListOfConstants

DjangoView = TypeVar('DjangoView', View, APIView)
RequestConst = TypeVar('RequestConst', req_const.WithQuery, req_const.WithoutQuery, ListOfConstants)
ResponseConst = TypeVar('ResponseConst', res_const.WithQuery, req_const.WithoutQuery, ListOfConstants)
AnyConst = TypeVar('AnyConst', req_const.WithQuery, req_const.WithoutQuery, res_const.WithQuery, res_const.WithoutQuery)
