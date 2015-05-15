from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from conrec.views import Recommend, Test, Matrix

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recommend/', Recommend.as_view()),
    url(r'^test/', Test.as_view()),
    url(r'^matrix/', Matrix.as_view()),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'))
)
