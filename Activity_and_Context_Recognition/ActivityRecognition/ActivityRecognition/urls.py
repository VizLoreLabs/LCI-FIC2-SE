from django.conf.urls import patterns, include, url
from django.contrib import admin
from activity_server.views import HomeView, RESTView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^ac/$', RESTView.as_view()),
                       url(r'^$', HomeView.as_view()))
