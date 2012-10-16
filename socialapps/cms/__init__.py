import sys
import mimetypes

from socialapps.cms.registration import portal_types

mimetypes.add_type('application/x-rar-compressed', '.rar', False)
mimetypes.add_type('video/x-ms-wmv', '.wmv', False)
mimetypes.add_type('video/x-flv', '.flv', False)


LOADING = False

def autodiscover():
    """
    Goes and imports the portal type submodule of every app in INSTALLED_APPS
    to make sure the portal type set classes are registered correctly.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            __import__(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module('types', app_path)
        except ImportError:
            continue
        __import__("%s.types" % app)
        app_path = sys.modules["%s.types" % app]
    LOADING = False
