from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase

from socialapps.core.exceptions import *

class PortalTemplateBase(type):
    """This meta-class is just for sure the registry in the templates stack
    """
    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)

class PortalTypeBase(type):
    """This meta-class is just for sure the registry in the types stack
    """
    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)

        
class BaseDict(dict):
    
    def __init__(self, **kw):
        for k in kw.keys():
            self[k] = kw[k]
        dict.__init__(self)

    def __setattr__(self, name, val):
        self[name] = val

    def __getattr__(self, name):
        return self[name]

    def __repr__(self):
        return "<" + self.__class__.__name__ + ">: " + self['title']

class PortalTemplate(BaseDict):
    """
    name
        The identifier of the template
        
    title
        The title of the template. This is displayed to the user to select
        a template.

    path
        The relative path to the template file according to Django templating
        engine.

    image
         image preview of template
    """
    __metaclass__ = PortalTemplateBase
    
    name = ''
    title = ''
    path = ''
    image = '/static/images/types/template_default.png'

class PortalType(BaseDict):
    """
    name
        The type of the registered content type.

    title
        The title of the registered content type.

    global_addable
        if set to true instances of the content type can be added to the
        portal.

    subtypes
        Allowed sub types which can be added to instances of the content type.

    templates
        Allowed templates which can be selected for instances of the content
        type.

    default_template
        The default template which is assigned when a instance of the content
        type is created.
        
    icon
        an image to represent the portal type
    """
    __metaclass__ = PortalTypeBase
    
    name = ''
    title = ''
    global_addable = False
    subtypes = []
    templates = []
    default_template = None
    icon = '/static/images/types/icon_default.gif'
        
    def get_subtypes(self):
        """Returns all allowed sub types for the belonging content type.
        """
        return [(sub.type, sub.title) for sub in self.subtypes]

    def get_templates(self):
        """Returns all allowed templates for the belonging content type.
        """
        return [(sub.name, sub.title) for sub in self.templates]

class SiteTypes(object):
    """
    Dictionary that contains site types and their templates
    """
    _types = {}
    
    def get_registered(self):
        """
        Return all types registered as a tuple, you can used this for a field choice in a model
        """
        return tuple([(key._meta.verbose_name, self._types[key].title) for key in self._types.keys()])

    def get_portal_type(self, model):
        if model in self._types.keys():
            return self._types[model]
        raise NotRegistered(_("the model %s don't have portal type registered") % model._meta.verbose_name )

    def registry(self, model, type):
        if isinstance(type, PortalTypeBase):
            if model in self._types.keys():
                raise AlreadyRegistered(_('The portal type %s has already been registered.') % model._meta.verbose_name)
            setattr(model, 'portal_type', type)
            self._types[model] = type
        else:
            raise ImproperlyConfigured(_("is not a portal type"))

    def unregistry(self, model):
        if isinstance(model, ModelBase):
            if not model in self._types.keys():
                raise NotRegistered(_("The %s is not registered") % model._meta.verbose_name)
            del self._types[model]
        else:
            raise ImproperlyConfigured(_("is not a portal type"))

portal_types = SiteTypes()
