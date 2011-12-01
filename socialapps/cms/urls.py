from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

from socialapps.cms.views import *

if settings.APPEND_SLASH:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)/$' , login_required(BaseContentView.as_view()), name="base_view")
else:
    base = url(r'^(?P<path>[0-9A-Za-z-_.//]+)$' , login_required(BaseContentView.as_view()), name="base_view")

urlpatterns = patterns('',
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)edit/$' , login_required(BaseContentEdit.as_view()), name="base_edit"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)delete/$' , login_required(BaseContentDelete.as_view()), name="base_delete"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)add/$' , login_required(BaseContentAdd.as_view()), name="base_add"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)add/(?P<portal_type>.+)/$' , login_required(BaseContentEdit.as_view()), name="base_create"),
    url( r'^(?P<path>[0-9A-Za-z-_.//]+)browser/(?P<portal_type>.+)/$' , login_required(ShowBrowser.as_view()), name="ajax_browser"),
    base,
)
