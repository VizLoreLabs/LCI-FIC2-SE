from django.conf.urls import patterns, include, url
from django.contrib import admin
from activity_server.views import HomeView, RESTView
from activity_server.hidden_views import HiddenRestView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^ac/$', RESTView.as_view()),
                       url(r'^hac/$', HiddenRestView.as_view()),
                       url(r'^$', HomeView.as_view()))
