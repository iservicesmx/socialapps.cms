from socialapps.cms.models import BaseContent

def get_slug(path):
    """
    Return the object's slug

        >>> get_slug('/foo/bar/')
        bar
    """
    if path.endswith('/'):
        path = path[:-1]
    return path.split("/")[-1]

def get_object(path):
    """
    Return the object
        
        >>> get_object('/foo/bar/')
        BaseContent at ...
    """
    slug = get_slug(path)
    obj = BaseContent.objects.get(slug=slug)
    # if obj is none raise 404
    # if no is none, get the portal_type
    # and return de correct type object
    
    
class CMSBaseView(TemplateView):
    object = None
    parent = None
    
    def get_context_data(self, **kwargs):
        kwargs.update({
                'context': self.object,
                'parent': self.
        })
    # en el dispatch obtener el object
    
    def get_template_names(self):
        if self.template_name is None:
            return self.object.get_templates()
        else:
            return [self.template_name]
    # obtener el template
    # renderear con el template
    
    
class CMSEditView(object):
    pass