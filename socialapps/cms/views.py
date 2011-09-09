from socialapps.cms.models import BaseContent
from django.views.generic import TemplateView
    
class CMSBaseView(TemplateView):
    object = None
    parent = None
    
    def get_context_data(self, **kwargs):
        kwargs.update({
                'object': self.object,
                'parent': self.parent,
        })
    # en el dispatch obtener el object
    
    def get_template_names(self):
        if not self.object:
            self.object = self.get_object()

        if self.template_name is None:
            return self.object.get_template()
        else:
            return [self.template_name]
    # obtener el template
    # renderear con el template

    def get_object(self):
        path = self.kwargs.get('path', None)
        obj = BaseContent.objects.get_base_object(path)
        return obj.get_object()
    
class CMSEditView(object):
    pass
