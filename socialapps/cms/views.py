from socialapps.cms.models import BaseContent
from django.views.generic.edit import FormView, DeleteView
from django.views.generic import TemplateView
from .registration import portal_types
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from tagging.models import Tag
from socialapps.core.utils import python_to_json
from socialapps.core.views import JSONTemplateView


class BaseContentSort(JSONTemplateView):
    def post(self, request, **kwargs):
        obj = BaseContent.objects.get(id = int(request.POST.get("object")))
        target = BaseContent.objects.get(id= int(request.POST.get("target")))
        position = request.POST.get("position")
        print obj
        print target
        print position
        print obj.move_to(target, position = position)
        return self.render_to_response("holaa")

class BaseContentView(JSONTemplateView):
    object = None
    parent = None
    children = None

    def get(self, request, **kwargs):
        if not self.object:
            self.object = self.get_object()
            self.children = self.object.get_object_children()
            self.parent = self.object.parent
        self.context = self.get_context_data()
        return self.render_to_response(self.context)
    
    def get_context_data(self, **kwargs):
        if self.request.is_ajax():
            if self.object.portal_type == 'image':
                sizes = []
                for size in self.object.image.sizes:
                    sizes.append({'size': '%dx%d' % size, 'url': getattr(self.object.image, 'url_%dx%d' % size)})
                return {'object' : self.object.image.url_128x128, 'sizes': sizes }
            else:
                return{'title': self.object.title, 'url': '/'+self.object.get_absolute_url() }
        else:
            kwargs.update({
                    'object'    : self.object,
                    'parent'    : self.parent,
                    'children'  : self.children,
                    'ancestors' : self.object.get_object_ancestors()[2:]
            })
            return kwargs
    
    def get_template_names(self):
        if self.template_name is None:
            return self.object.get_template()
        else:
            return [self.template_name]

    def get_object(self):
        path = self.kwargs.get('path', None)
        return BaseContent.objects.get_base_object(path)
        
class ShowBrowser(BaseContentView):
    def get_template_names(self):
        return 'cms/browser.html'
        
    def get_context_data(self, **kwargs):
        kwargs.update({
            'portal_type'   : self.kwargs.get('portal_type'),
        })
        return super(ShowBrowser, self).get_context_data(**kwargs)
        
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
            'title'         : self.get_portal_type().title,
            'add'           : self.add,
            'portal_type'   : self.get_portal_type().name,
        })
        return super(BaseContentEdit, self).get_context_data(**kwargs)
        
    def get_portal_type(self):
        if not self.object:
            return portal_types.get_portal_type(self.model)
        else:
            return self.object.get_portal_type()

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
                return BaseContent.objects.get_base_object(path)
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
            return BaseContent.objects.get_base_object(path)
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
        if self.object.portal_type == 'image' and not self.request.is_ajax():
            return HttpResponse(self.object.image.url_128x128)
        return HttpResponse(python_to_json({"success": True, "success_url": self.success_url}), content_type='application/json')        
        
    def form_invalid(self, form):
        return HttpResponse(python_to_json({"errors" : form.errors}), content_type='application/json')

class BaseContentDelete(DeleteView):
    template_name = "cms/confirm.html"
    object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseContentDelete, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseContentDelete, self).get(request, *args, **kwargs)

    def get_object(self):
        path = self.kwargs.get('path', None)
        return BaseContent.objects.get_base_object(path)

    def get_success_url(self):
        if self.object.parent:
            return "/%s" % self.object.parent.get_absolute_url()
        return "/"
        
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.title == 'resources':
            return HttpResponseRedirect('/%s' % self.object.get_absolute_url())
        return super(BaseContentDelete, self).delete(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        kwargs.update({
            'object'        : self.object,
            'url_form_post' : reverse('base_delete', kwargs={'path' : self.object.get_absolute_url() }),
        })
        return super(BaseContentDelete, self).get_context_data(**kwargs)

class BaseContentAdd(TemplateView):
    template_name = "cms/add.html"
    
    def get_object(self):
        path = self.kwargs.get('path', None)
        return BaseContent.objects.get_base_object(path)

    def get_context_data(self, **kwargs):
        kwargs = super(BaseContentAdd, self).get_context_data(**kwargs)
        type_container = []
        type_content = []
        for item in self.get_object().get_portal_type().subtypes:
            if not item.subtypes:
                type_content.append(item)
            else:
                type_container.append(item)
                
        if self.get_object().get_portal_type().name == 'folder':
            type_container.append(self.get_object().get_portal_type())
            
        kwargs.update({
            'path'          : self.kwargs.get('path', None),
            'type_container': type_container,
            'type_content'  : type_content,
        })
        return kwargs
