import tempfile

from django.db import models
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.exceptions import ImproperlyConfigured

from socialapps.cms.models import *
from socialapps.core.exceptions import *
from socialapps.cms.registration import PortalTemplate, PortalType, SiteTypes, portal_types
from socialapps.cms.registration import PortalTypeBase, PortalTemplateBase


class CMSModelsTest(TestCase):
    """
    """
    def setUp(self):
        pass
        
    def generate_image(self):
        """
        use:
            img = self.generate_image()
            object.image.save('test.jpeg', ContentFile(img.read()))
            img.close()
        """
        from PIL import Image
        tmp = tempfile.TemporaryFile()
        Image.new('RGB', (800, 600)).save(tmp, 'JPEG')
        tmp.seek(0)
        return tmp
        
    def test_models(self):
        folder1 = Folder.objects.create(title="Folder 1")
        folder1.save()
        folder1_1 = Folder.objects.create(title="Folder 1")
        folder1_1.save()
        
        self.assertEqual(folder1.slug,'folder-1')
        self.assertEqual(folder1_1.slug,'folder-1-1')
        
        subfolder1 = Folder.objects.create(title="SubFolder 1", parent=folder1)
        subfolder1.save()
        subsubfolder1 = Folder.objects.create(title="SubSubFolder 1", parent=subfolder1)
        subsubfolder1.save()
        
        self.assertEqual(folder1.get_absolute_url(), 'folder-1/')
        self.assertEqual(subfolder1.get_absolute_url(),'folder-1/subfolder-1/')
        self.assertEqual(subsubfolder1.get_absolute_url(),'folder-1/subfolder-1/subsubfolder-1/')
        
    def test_slug_different_model(self):
        item1 = Folder.objects.create(title="Item 1")
        item1.save()
        item1_1 = MultiPage.objects.create(title="Item 1", parent=item1)
        item1_1.save()
        self.assertEqual(item1.get_absolute_url(), 'item-1/')
        self.assertEqual(item1_1.get_absolute_url(), 'item-1/item-1-1/')


class Dummy(object):
    pass

class ItemModel(models.Model):
    foo = models.CharField("Foo", max_length=200, blank=True)

class ItemTemplate(PortalTemplate):
    name = 'item'
    title = 'Item Template'
    path = 'cms/item.html'
    image = '/static/images/types/item.png'

class ItemType(PortalType):
    name = "item"
    title = "Item"
    global_addable = False
    subtypes = []
    templates = [ItemTemplate,]
    default_template = ItemTemplate


class CMSPortalTypeTest(TestCase):
    
    def setUp(self):
        self.portal_type = SiteTypes()
        
        if not self.portal_type.get_registered():
            self.portal_type.registry(ItemModel, ItemType)
        
    def test_register_portal_type(self):
            
        self.assertTrue(isinstance(ItemTemplate, PortalTemplateBase))
        self.assertTrue(isinstance(ItemType, PortalTypeBase))
        self.assertEqual(ItemType.name,'item')
        
        def raise1():
            self.portal_type.registry(ItemModel, Dummy)
        
        self.assertRaises(ImproperlyConfigured, raise1)
        self.assertTrue(self.portal_type.get_portal_type(ItemModel) is ItemType)
        self.assertEqual(self.portal_type.get_portal_type(ItemModel).name, 'item')
        self.assertEqual(len(self.portal_type.get_registered()), 1 )
        self.assertEqual(self.portal_type.get_registered(), (('item model','Item'),))
        
        def raise2():
            self.portal_type.registry(ItemModel, ItemType)
        
        self.assertRaises(AlreadyRegistered, raise2)
        
        def raise3():
            self.portal_type.unregistry(ItemType)
        
        self.assertRaises(ImproperlyConfigured, raise3)
        self.portal_type.unregistry(ItemModel)
        
        def raise4():
            self.portal_type.unregistry(ItemModel)
        self.assertRaises(NotRegistered, raise4)
        
    def _portal_type_templates(self):
                
        portal_type = ItemModel.portal_type
        self.assertTrue(len(portal_type.templates) == 1 )
        self.assertTrue(ItemTemplate in portal_type.templates)
        self.assertTrue(portal_type.default_template is ItemTemplate)
        
        template = portal_type.default_template
        self.assertEqual(template.name, 'item')

