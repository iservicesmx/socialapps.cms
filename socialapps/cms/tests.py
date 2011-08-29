import tempfile

from django.test import TestCase
from django.core.files.base import ContentFile

from socialapps.cms.models import *

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

from socialapps.cms.registration import PortalTemplate, PortalType, SiteTypes, portal_types

class CMSPortalTypeTest(TestCase):
    
    def setUp(self):
        self.portal_type = SiteTypes()
        
    def test_register_portal_type(self):
        
        class ItemTemplate(PortalTemplate):
            name = 'item'
            title = 'Item Template'
            path = 'cms/item.html'
            image = '/static/images/types/item.png'
        
        class ItemType(PortalType):
            type = "item"
            title = "Item"
            global_addable = False
            subtypes = []
            templates = [ItemTemplate,]
            default_template = ItemTemplate
            
        self.assertTrue(isinstance(ItemTemplate, PortalTemplate))
        self.assertTrue(isinstance(ItemType, PortalType))
        