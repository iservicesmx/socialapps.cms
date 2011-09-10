from django.db import models 
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.files.base import ContentFile
from django.core.exceptions import ImproperlyConfigured

from ..models import *
from socialapps.core.exceptions import *
from ..registration import portal_types
from .. import autodiscover
from ..types import *
autodiscover()

#print portal_types.get_registered()

class CMSViewTest(TestCase):
    urls = "socialapps.cms.tests.urls"

    def setUp(self):
        self.client = Client()
        pass

    def test_views(self):
        folder = Folder.objects.create(title="folder 1", status = 1, portal_type="folder")
        folder.save()
        response = self.client.get(reverse('base_view', kwargs={'path' : 'folder-1/'}))
        self.assertEqual(response.status_code, 200)

        folder2 = Folder.objects.create(title="folder 2", status = 1, portal_type="folder", parent=folder)
        folder2.save()
        response = self.client.get(reverse('base_view', kwargs={'path' : '/folder-1/folder-2/'}))
        self.assertEqual(response.status_code, 200)

        children = folder.get_children()
        self.assertTrue(folder2 in [c.get_type_object() for c in children])

