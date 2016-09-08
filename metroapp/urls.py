# pylint: disable=invalid-name
from django.conf.urls import url

from .views import HomeView

urlpatterns = [
    url(r'^', HomeView.as_view(), name='home-view'),
]
