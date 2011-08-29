class MetaTypeBase(type):
    def __new__(meta, classname, bases, classDict):
        #print 'Class Name:', classname
        #print 'Bases:', bases
        #print 'Class Attributes', classDict
        return type.__new__(meta, classname, bases, classDict)
        
class BaseDict(dict):
    __metaclass__ = MetaTypeBase
    
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
    
    name = ''
    title = ''
    global_addable = False
    subtypes = []
    templates = []
    default_template = None
    icon = '/static/images/types/icon_default.gif'
    
    # Esto va en el register
    #def __init__(self, **kwargs):
    #    if not kwargs.has_key('name'):
    #        kwargs['name'] = model._meta.label.lower
    #        
    #    return super(PortalType, self).__init__(**kwargs)
    
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
    def registry(self, model, type):
        pass
    
portal_types = SiteTypes()
