from socialapps.cms.models import BaseContent
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
    
class BaseContentView(TemplateView):
    object = None
    parent = None
    children = None

    def get(self, request, **kwargs):
        if not self.object:
            self.object = self.get_object()
            self.children = [child.get_type_object() for child in self.object.get_children()]
        self.context = self.get_context_data()
        return self.render_to_response(self.context)
    
    def get_context_data(self, **kwargs):
        kwargs.update({
                'object'    : self.object,
                'parent'    : self.parent,
                'children'  : self.children,
        })
        return kwargs
    
    def get_template_names(self):
        if self.template_name is None:
            return self.object.get_template()
        else:
            return [self.template_name]

    def get_object(self):
        path = self.kwargs.get('path', None)
        obj = BaseContent.objects.get_base_object(path)
        return obj.get_type_object()
    
class BaseContentEdit(FormView):
    pass

