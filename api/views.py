from django.shortcuts import render
from django.views import View

from ..adapters.repositories import NamespacesRepository
from ..serializers.serializers import NameSpaceSerializer
from ..utilities.custom_typing import HttpRequest, HttpResponse


class ApyWyHomePageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        namespaces = NamespacesRepository.all()
        serializer = NameSpaceSerializer(namespaces=namespaces)
        context = serializer.data
        return render(request, template_name='apywy/index.html', context=context)
