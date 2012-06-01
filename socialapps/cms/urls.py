from django.conf.urls.defaults import *
from django.conf import settings

from socialapps.cms.views import *

if settings.APPEND_SLASH:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)/$' , BaseContentView.as_view(), name="base_view")
else:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)$' , BaseContentView.as_view(), name="base_view")

urlpatterns = patterns('',
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)edit/$' , BaseContentEdit.as_view(), name="base_edit"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)delete/$' , BaseContentDelete.as_view(), name="base_delete"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)add/$' , BaseContentAdd.as_view(), name="base_add"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)add/(?P<portal_type>.+)/$' , BaseContentEdit.as_view(), name="base_create"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)browser/(?P<portal_type>.+)/$' , ShowBrowser.as_view(), name="ajax_browser"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)sort/$', BaseContentSort.as_view(), name="base_sort"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)get_image_thumb/(?P<size>.+)/$', ImageThumb.as_view(), name="image_thumb"),
    base,
)
