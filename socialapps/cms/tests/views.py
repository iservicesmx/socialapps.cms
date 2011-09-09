from django.db import models 
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.files.base import ContentFile
from django.core.exceptions import ImproperlyConfigured

from ..models import *
from socialapps.core.exceptions import *
from ..registration import PortalTemplate, PortalType, SiteTypes, portal_types
from ..registration import PortalTypeBase, PortalTemplateBase


class CMSViewTest(TestCase):
    urls = "socialapps.cms.tests.urls"

    def setUp(self):
        self.client = Client()
        pass

    def test_views(self):
        folder = Folder.objects.create(title="folder 1")
        folder.save()
        response = self.client.get(reverse('base_view', kwargs={'path' : 'folder-1/'}))
        self.assertEqual(response.status_code, 200)
