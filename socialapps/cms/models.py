import unicodedata
import re

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.template.loader import select_template

from socialapps.cms import mimetypes
from socialapps.core.models import BaseMetadata
from socialapps.core.utils import bleach_clean

from .registration import portal_types
from .managers import BaseContentManager
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
    hide        = models.BooleanField(_('Hide item'), default=False)
    pagination  = models.PositiveIntegerField(_(u'Number of children per page'), default=0)
    site        = models.ForeignKey(Site, default=settings.SITE_ID)
    
    objects = BaseContentManager()
    
    class Meta:
        unique_together = ('parent', 'slug')
        ordering = ('tree_id', 'lft')
    
    class MPTTMeta:
        order_insertion_by = 'slug'
                
    def get_object_children(self, show_all=False, **kwargs):
        if not show_all:
            children = self.get_children().filter(hide=False, **kwargs)
        else:
            children = self.get_children().filter(**kwargs)
        return [child.get_type_object() for child in children]
        
    def get_object_ancestors(self):
        ancestors = self.get_ancestors()
        return [ancestor.get_type_object() for ancestor in ancestors]

    def get_parents(self, include_self=False):
        parents = []
        temp = self
        while temp:
            parents.append(temp)
            if not temp.parent:
                parents.reverse()
                if include_self:
                    return parents
                return parents[:-1]
            temp = temp.parent

    def save(self, *args, **kwargs):
        if not self.portal_type:
            self.portal_type = self.get_portal_type().name
        
        if not self.slug:
            #concrete_model = base_concrete_model(BaseContent, self)
            self.slug = self.get_slug()
            i = 1
            #while concrete_model.objects.filter(slug=self.slug, parent=self.parent).count() > 0:
            while BaseContent.objects.filter(slug=self.slug, parent=self.parent, site=self.site).count() > 0:
                self.slug = self.get_slug() + "-%s" % i
                i += 1
        
        super(BaseContent, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/".join([ancestor.slug for ancestor in self.get_parents(True)])

    def get_type_object(self):
        if self.__class__.__name__.lower() == "basecontent":
            return getattr(self, self.portal_type)
        else:
            return self
        
    def get_portal_type(self):
        return portal_types.get_portal_type(self.__class__)
        
    def get_template(self, template_name=None):
        if not self.template:
            pt = portal_types.get_portal_type(self.__class__)
            if template_name:
                for template in pt.templates:
                    if template.name == pt.default_template.name + '_admin':
                        temp = select_template([template.path, pt.default_template.path])
                        return temp.name
            return pt.default_template.path
        return self.template
        
    def get_icon(self):
        """Get the default icon predefined at PortalType"""
        return self.get_portal_type().icon
        
    icon = property(get_icon, doc=get_icon.__doc__)
        
class FolderRoot(BaseContent):
    class Meta:
        abstract = True

class Folder(BaseContent):
    pass
    
class MultiPage(BaseContent):
    show_toc = models.BooleanField(default=False)

class Page(BaseContent):
    text = models.TextField(_(u"Text"), blank=True)

    def save(self, *args, **kwargs):
        self.text = bleach_clean(self.text)
        return super(Page, self).save(*args, **kwargs)
        
class Image(BaseContent):
    image = models.ImageField(_(u"Image"), upload_to="uploads")
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image.name = ''.join((c for c in unicodedata.normalize('NFD', self.image.name) if unicodedata.category(c) != 'Mn'))
                if not self.title:
                    self.title = self.image.name
        return super(Image, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Image)
def delete_image(sender, **kwargs):
    instance = kwargs['instance']
    if instance.image:
        instance.image.delete()

class File(BaseContent):
    file = models.FileField(upload_to="files", max_length=255)
    mimetype = models.CharField(max_length = 200, blank = True, null = True)
    true_mimetype = models.CharField(max_length = 200, blank = True, null = True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = ''.join((c for c in unicodedata.normalize('NFD', self.file.name) if unicodedata.category(c) != 'Mn'))
            if not self.title:
                self.title = self.file.name
            # super(File, self).save(*args, **kwargs)
            mimetype = mimetypes.guess_type(self.file.path, False)
            if mimetype[0]:
                file_type = re.search("\w+", mimetype[0]).group()
                self.mimetype = file_type
                self.true_mimetype = mimetype[0]
        return super(File, self).save(*args, **kwargs)

    @property
    def filename(self):
        return os.path.split(self.file.name)[1]

@receiver(pre_delete, sender=File)
def delete_file(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        instance.file.delete()
        
class Link(BaseContent):
    url = models.URLField(_("Link"), verify_exists = False)
    frame = models.BooleanField(_('frame'), default=False)
    redirect = models.BooleanField(_("Redirect"), default=False)
