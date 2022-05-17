from django.shortcuts import render
from django.views import View

from ..service_layer.initializers import NameSpacesInitializer
from ..service_layer.serializers import NameSpaceSerializer
from ..utilities.custom_typing import HttpRequest, HttpResponse


class ApyWyHomePageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        namespaces = NameSpacesInitializer.NAMESPACES
        serializer = NameSpaceSerializer(namespaces=namespaces)
        context = serializer.data
        return render(request, template_name='ApyWy/index.html', context=context)
