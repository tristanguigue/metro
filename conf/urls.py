from django.conf.urls import include, url
import metroapp.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', metroapp.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
