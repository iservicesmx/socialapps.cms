from socialapps.cms.models import BaseContent
from django.views.generic.edit import FormView, DeleteView
from django.views.generic import TemplateView
from .registration import portal_types
from django.http import Http404
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from tagging.models import Tag
    
class BaseContentView(TemplateView):
    object = None
    parent = None
    children = None

    def get(self, request, **kwargs):
        if not self.object:
            self.object = self.get_object()
            self.children = [child.get_type_object() for child in self.object.get_children()]
            self.parent = self.object.parent
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
    form_class = None
    template_name = None
    model = None
    parent = None
    object = None
    url_form_post = None
    add = None

    def check_create_or_update(self):
        if 'portal_type' in self.kwargs:
            return True
        else:
            return False

    def get_url_form_post(self):
        if self.add:
            return reverse('base_create', kwargs={'path' : self.parent.get_absolute_url(), 'portal_type' : self.kwargs.get('portal_type', None)})
        else:
            return reverse('base_edit', kwargs={'path' : self.object.get_absolute_url()})

    def get_success_url(self):
        return "/%s" % self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.add = self.check_create_or_update()
        self.object = self.get_object()
        self.model = self.get_model()
        self.parent = self.get_parent_object()
        return super(BaseContentEdit, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.add = self.check_create_or_update()
        self.object = self.get_object()
        self.model = self.get_model()
        self.parent = self.get_parent_object()
        return super(BaseContentEdit, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BaseContentEdit, self).get_form_kwargs()
        if self.object:
            kwargs.update({
                'instance' : self.object,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'parent'        : self.parent,
            'url_form_post' : self.get_url_form_post(),
            'tags'          : Tag.objects.all().values_list('name', flat=True),
        })
        return super(BaseContentEdit, self).get_context_data(**kwargs)

    def get_model(self):
        if not self.model:
            if self.add:
                return portal_types.get_model(self.kwargs.get('portal_type'))
            else:
                return self.object.__class__
        return self.model

    def get_object(self):
        if not self.object:
            if not self.add:
                path = self.kwargs.get('path', None)
                obj = BaseContent.objects.get_base_object(path)
                return obj.get_type_object()
            else:
                return None
        return self.object

    def get_form_class(self):
        if not self.form_class:
            return portal_types.get_portal_type(self.model).edit_form
        return self.form_class 

    def get_template_names(self):
        if not self.template_name:
            return "cms/edit_form.html"
        return self.template_name
    
    def get_parent_object(self):
        if not self.parent:
            path = self.kwargs.get('path', None)
            obj = BaseContent.objects.get_base_object(path)
            return obj.get_type_object()
        return self.parent

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.creator = self.request.user
        self.object.tags = ' '.join(self.request.POST.get('tags', '').split(','))
        if self.add:
            self.object.parent = self.parent
            self.object.portal_type = self.kwargs.get('portal_type', None)
        self.object.save()
        self.success_url = self.get_success_url()
        return super(BaseContentEdit, self).form_valid(form)

class BaseContentDelete(DeleteView):
    template_name = "cms/confirm.html"

    def get_object(self):
        path = self.kwargs.get('path', None)
        obj = BaseContent.objects.get_base_object(path)
        return obj.get_type_object()

    def get_success_url(self):
        if self.object.parent:
            return "/%s" % self.object.parent.get_absolute_url()
        return "/"

class BaseContentAdd(TemplateView):
    template_name = "cms/add.html"
    
    def get_object(self):
        path = self.kwargs.get('path', None)
        return BaseContent.objects.get_base_object(path).get_type_object()

    def get_context_data(self, **kwargs):
        kwargs = super(BaseContentAdd, self).get_context_data(**kwargs)
        
        type_container = []
        type_content = []
        for item in self.get_object().get_portal_type().subtypes:
            if not item.subtypes:
                type_content.append(item)
            else:
                type_container.append(item)
            
        kwargs.update({
            'path'          : self.kwargs.get('path', None),
            'type_container': type_container,
            'type_content'  : type_content,
        })
        return kwargs
