from django.conf.urls.defaults import *

from socialapps.cms.views import *

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', CMSBaseView.as_view(), name="base_view"),
)
