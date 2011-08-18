from django.test import TestCase
from socialapps.cms.models import *

class CMSModelsTest(TestCase):
    """
    """
    def setUp(self):
        pass
        
    def test_models(self):
        folder1 = Folder.objects.create(title="Folder 1")
        folder1.save()
        folder1_1 = Folder.objects.create(title="Folder 1")
        folder1_1.save()
        
        self.assertEqual(folder1.slug,'folder-1')
        self.assertEqual(folder1_1.slug,'folder-1-1')
        
        
    