from django.shortcuts import render
from django.views import View

from ..service_layer.initializers import NameSpacesInitializer
from ..service_layer.serializers import NameSpaceSerializer
from ..utilities.custom_typing import HttpRequest, HttpResponse


class ApyWyHomePageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        namespaces = NameSpacesInitializer.NAMESPACES    # type: ignore
        serializer = NameSpaceSerializer(namespaces=namespaces)
        context = serializer.data
        return render(request, template_name='apywy/index.html', context=context)
