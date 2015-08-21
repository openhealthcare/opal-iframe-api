"""
Urls for the iframeapi OPAL plugin
"""
from django.conf.urls import patterns, url
from iframeapi import views

urlpatterns = patterns(
    '',
    url('^iframeapi/$', views.iframe_api, name="iframe_api"),
)
