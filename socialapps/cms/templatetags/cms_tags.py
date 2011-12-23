from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag("cms/portlet_menu.html")
def portlet_menu(object):
	return {
		'object' : object,
	}