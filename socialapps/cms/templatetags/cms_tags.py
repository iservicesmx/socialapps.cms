from django import template
import re

register = template.Library()

@register.inclusion_tag("cms/navigation_portlet.html")
def show_navigation(obj):
    if not hasattr(obj,'get_local_menu'):
        while not hasattr(obj,'get_local_menu'):
            obj = obj.parent.get_type_object()
    return { 'menu' : obj.get_local_menu(), 'absolute_url': obj.get_absolute_url()}

@register.simple_tag(takes_context=True)
def get_content_parent(context, obj):
    for item in obj.get_ancestors(include_self=True, ascending=True):
        if item.slug in ['syllabus', 'resources', 'discussionroot', 'files']:
            context['content_parent'] = item
            return ""