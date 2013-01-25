from django import template
from permissions.utils import has_permission

register = template.Library()


@register.inclusion_tag("cms/navigation_portlet.html", takes_context=True)
def show_navigation(context, obj):
    path_items = context['request'].path.split("/")
    absolute_url = obj.get_absolute_url()
    if "courses" in path_items and ("resources" in path_items or "syllabus" in path_items):
        section = context['request'].session.get('current_section')
        if section:
            if section['section'].parent in obj.get_ancestors(include_self=True, ascending=True):
                obj = section['section']
                absolute_url = section['path']
    if not hasattr(obj, 'get_local_menu'):
        while not hasattr(obj, 'get_local_menu'):
            if obj.parent:
                obj = obj.parent.get_type_object()
                absolute_url = obj.get_absolute_url()
            else:
                return None
    return {'menu': obj.get_local_menu(context['user']), 'absolute_url': absolute_url}


@register.inclusion_tag("cms/breadcrumb.html")
def show_breadcrumb(obj):
    ancestors = obj.get_parents()[1:]
    anc = []
    if len(ancestors) > 2:
        anc.append(ancestors[0])
        anc.append(None)
        anc.append(ancestors[-1])
    else:
        anc = ancestors
    return {
        'object':       obj,
        'ancestors':    ancestors,
    }

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
