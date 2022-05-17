from django.urls import path

from . import views

urlpatterns = [
    path('', views.ApyWyHomePageView.as_view(), name='apywy_home_page'),
]
