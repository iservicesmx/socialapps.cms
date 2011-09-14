from socialapps.cms.models import BaseContent
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .registration import portal_types
from django.http import Http404
from django.forms.models import model_to_dict
    
class BaseContentView(TemplateView):
    object = None
    parent = None
    children = None

    def get(self, request, **kwargs):
        if not self.object:
            self.object = self.get_object()
#            self.children = [child.get_type_object() for child in self.object.get_children()]
        self.context = self.get_context_data()
        return self.render_to_response(self.context)
    
    def get_context_data(self, **kwargs):
        kwargs.update({
                'object'    : self.object,
                'parent'    : self.parent,
#                'children'  : self.children,
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
    form_class = None
    template_name = None
    model = None
    parent = None
    object = None

    def get(self, request, **kwargs):
        if not 'portal_type' in kwargs:
            self.object = self.get_object()
        else:
            self.object = None
        self.get_model()
        self.get_form_class()
        self.get_template_name()
        self.get_parent_object()
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form'  : self.form_class(instance=self.object),
            'parent': self.parent,
        })
        return super(BaseContentEdit, self).get_context_data(**kwargs)

    def get_model(self):
        if not self.model:
            portal_type = self.kwargs.get('portal_type', None)
            if portal_type:
                self.model = portal_types.get_model(portal_type)
        return self.model

    def get_object(self):
        path = self.kwargs.get('path', None)
        obj = BaseContent.objects.get_base_object(path)
        return obj.get_type_object()

    def get_form_class(self):
        if not self.form_class:
            if 'portal_type' in self.kwargs:
                self.form_class = self.model().get_edit_form
            else:
                self.form_class = self.object.get_edit_form
        return self.form_class 

    def get_template_name(self):
        if not self.template_name:
            self.template_name = "cms/edit_form.html"
        return self.template_name
    
    def get_parent_object(self):
        if not self.parent:
            path = self.kwargs.get('path', None)
            obj = BaseContent.objects.get_base_object(path)
            self.parent = obj.get_type_object()
        return self.parent
            
