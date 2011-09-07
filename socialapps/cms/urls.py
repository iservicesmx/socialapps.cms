from django.conf.urls.defaults import *

from socialapps.cms.views import *

urlpatterns = patterns('socialapps.cms.views',
    url(r'^(?P<path>.*)$', "base_view", name="base_view"),
)
