from django import template
from permissions.utils import has_permission
import re

register = template.Library()

@register.inclusion_tag("cms/navigation_portlet.html")
def show_navigation(obj):
    if not hasattr(obj,'get_local_menu'):
        while not hasattr(obj,'get_local_menu'):
            obj = obj.parent.get_type_object()
    return { 'menu' : obj.get_local_menu(), 'absolute_url': obj.get_absolute_url()}
    
@register.inclusion_tag("cms/breadcrumb.html")
def show_breadcrumb(obj):
    return {
        'object'    : obj,
        'ancestors' : obj.get_object_ancestors()[1:],
    }
    

@register.simple_tag(takes_context=True)
def get_content_parent(context, obj):
    for item in obj.get_ancestors(include_self=True, ascending=True):
        if item.slug in ['syllabus', 'resources', 'discussionroot', 'files']:
            context['content_parent'] = item
            return ""
            
@register.inclusion_tag("cms/multipage_toc.html", takes_context=True)
def show_multipage_toc(context, obj):
    for item in obj.get_ancestors(include_self=True, ascending=True):
        if item.portal_type == 'multipage':
            if has_permission(item, context['user'], 'edit') and context['request'].GET.get('template', None) != 'user':
                context['toc'] = item.get_object_children(True)
            else:
                context['toc'] = item.get_object_children(False)
            return context
    return False