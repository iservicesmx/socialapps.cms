from django.db import models 
from django.contrib.auth.models import User
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


class CMSViewTest(TestCase):
    urls = "socialapps.cms.tests.urls"


    def setUp(self):
        self.client = Client()
        user = User.objects.create_user("user", "dummy@mail.com", "password")
        self.client.login(username="user", password="password")

    def test_list_views(self):
        folder = Folder.objects.create(title="folder 1", status = 1, portal_type="folder")
        folder.save()
        response = self.client.get(reverse('base_view', kwargs={'path' : 'folder-1/'}))
        self.assertTemplateUsed(response, 'cms/folder.html')

        folder2 = Folder.objects.create(title="folder 2", status = 1, portal_type="folder", parent=folder)
        folder2.save()
        response = self.client.get(reverse('base_view', kwargs={'path' : '/folder-1/folder-2/'}))
        self.assertTemplateUsed(response, 'cms/folder.html')

        children = folder.get_children()
        self.assertTrue(folder2 in [c.get_type_object() for c in children])

    def test_edit_view(self):
        folder = Folder.objects.create(title="folder 1", status=1, portal_type="folder")
        folder.save()
        response=self.client.get(reverse('base_edit', kwargs={'path' : '/folder-1/'}))
        self.assertTemplateUsed(response, "cms/edit_form.html")

