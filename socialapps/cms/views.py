from socialapps.cms.models import BaseContent
    
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