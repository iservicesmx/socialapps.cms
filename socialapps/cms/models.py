from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from socialapps.core.models import BaseMetadata
from socialapps.core.fields import ImageWithThumbsField
from .registration import portal_types

from .managers import BaseContentManager
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag

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
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
            (ACTIVE,    _('Active')),
            (INACTIVE,  _('Inactive')),
    )
    
    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children')
    portal_type = models.CharField(_(u"Portal type"), max_length=100, blank=True)
    template    = models.CharField(_(u"Template"), max_length=200, blank=True)
    status      = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=ACTIVE)
    
    objects = BaseContentManager()
    
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
        url = "/".join([ancestor.slug for ancestor in self.get_ancestors(include_self=True)]) + "/"
        return url
    
    def get_type_object(self):
        if self.__class__.__name__.lower() == "basecontent":
            return getattr(self, self.portal_type)
        else:
            return self
        
    def get_portal_type(self):
        return portal_types.get_portal_type(self.__class__)
        
    def get_template(self):
        if not self.template:
            pt = portal_types.get_portal_type(self.__class__)
            return pt.default_template.path
        return self.template
        
    def get_contenttype(self):
        return ContentType.objects.get_for_model(self).id
        
class FolderRoot(BaseContent):
    class Meta:
        abstract = True

class Folder(BaseContent):
    pass
    
class MultiPage(BaseContent):
    show_toc = models.BooleanField(default=False)

class Page(BaseContent):
    text = models.TextField(_(u"Text"), blank=True)
        
class Image(BaseContent):
    image = ImageWithThumbsField(_(u"Image"), upload_to="uploads",
        sizes=((64, 64), (128, 128), (400, 400), (600, 600), (800, 800)))

#    def get_absolute_url(self):
#        return 
#        pass

#    get_absolute_url = models.permalink(get_absolute_url)

class File(BaseContent):    
    file = models.FileField(upload_to="files")

#    def get_absolute_url(self):
#        return reverse("socialapps_file", kwargs={"id" : self.id})

    @property
    def filename(self):
        return os.path.split(self.file.name)[1]
