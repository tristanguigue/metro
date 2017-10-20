# pylint: disable=invalid-name
from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from .views import ContactView, ExplanationView, HomeView, MethodologyView, RelevanceView
from .views import set_language_from_url

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home-view'),
    url(r'^methodology', MethodologyView.as_view(), name='methodology-view'),
    url(r'^relevance', RelevanceView.as_view(), name='relevance-view'),
    url(r'^explanation', ExplanationView.as_view(), name='explanation-view'),
    url(r'^contact', ContactView.as_view(), name='contact-view'),
    url(r'^setlang/(?P<user_language>\w+)/$', set_language_from_url, name='set_language_from_url'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
