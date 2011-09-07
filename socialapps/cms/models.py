from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from socialapps.core.models import BaseMetadata
from socialapps.core.fields import ImageWithThumbsField

class BaseContent(MPTTModel, BaseMetadata):
    """Base content object. From this class all content types should inherit.
    
    **Attributes:**
    parent
        required by MPTT
    
    portal_type
        The portal type of the specific content object.
        
    template
        The current selected template of the object.
    """
    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children')
    #portal_type = models.CharField(_(u"Portal type"), max_length=100, blank=True)
    template    = models.CharField(_(u"Template"), max_length=200, blank=True)
    
    class Meta:
        unique_together = ('parent', 'slug')
        ordering = ('tree_id', 'lft')
    
    class MPTTMeta:
        unique_together = ('parent', 'slug')
        ordering = ('tree_id', 'lft')
        order_insertion_by = 'slug'
    
    def save(self, *args, **kwargs):        
        super(BaseContent, self).save(*args, **kwargs)
    

    def get_absolute_url(self):
        url = ("/").join([ancestor.slug for ancestor in self.get_ancestors(include_self=True)]) + '/'
        
        return url
        #return reverse('base_view', url)
    
    def get_object(self):
        if self.__class__.__name__.lower() == "basecontent":
            return getattr(self, self.portal_type)
        else:
            return self
        
    def get_portal_type(self):
        #acceder al registro y traer a la clase base
        pass
        
    def get_template(self):
        pass
        
class Folder(BaseContent):
    pass
    
class MultiPage(BaseContent):
    show_toc = models.BooleanField(default=False)

class Page(BaseContent):
    text = models.TextField(_(u"Text"), blank=True)
        
class Image(BaseContent):
    image = ImageWithThumbsField(_(u"Image"), upload_to="uploads",
        sizes=((64, 64), (128, 128), (400, 400), (600, 600), (800, 800)))

    def get_absolute_url(self):
        pass
    get_absolute_url = models.permalink(get_absolute_url)    

class File(BaseContent):    
    file = models.FileField(upload_to="files")

    def get_absolute_url(self):
        return reverse("socialapps_file", kwargs={"id" : self.id})

    @property
    def filename(self):
        return os.path.split(self.file.name)[1]