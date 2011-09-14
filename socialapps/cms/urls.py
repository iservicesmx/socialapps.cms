from django.conf.urls.defaults import *
from django.conf import settings

from socialapps.cms.views import *

if settings.APPEND_SLASH:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)/$' , BaseContentView.as_view(), name="base_view")
else:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)$' , BaseContentView.as_view(), name="base_view")

urlpatterns = patterns('',
    base,
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)edit$' , BaseContentEdit.as_view(), name="base_edit"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)/add/(?P<portal_type>.+)$' , BaseContentEdit.as_view(), name="base_add"),
)
