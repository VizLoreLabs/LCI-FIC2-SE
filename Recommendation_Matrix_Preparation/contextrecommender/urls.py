from django.conf.urls import patterns, include, url
from django.contrib import admin
from conrec.views import Recommend

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recommend/', Recommend.as_view()),
)
