from django import template
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def get_content_parent(context, obj):
    for item in obj.get_ancestors(include_self=True, ascending=True):
        if item.slug in ['syllabus', 'resources', 'discussionroot', 'files']:
            context['content_parent'] = item
            return ""