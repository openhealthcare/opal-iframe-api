from iframeapi.urls import urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

# a dummy url conf so that we can use url look ups to the admin in the tests
# like in production

admin.autodiscover()

urlpatterns += patterns(
    '',
    url(r'^admin/?', include(admin.site.urls)),
)
