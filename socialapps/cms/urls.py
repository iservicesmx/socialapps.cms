from django.conf.urls.defaults import *

# URL patterns for socialapps.cms

urlpatterns = patterns('socialapps.cms.views',
    url(r'^(?P<path>.*)$', "base_view", name="base_view"),
    url(r'^$', "base_view", name="base_view"),
)
