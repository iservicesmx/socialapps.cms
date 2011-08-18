from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from socialapps.core.models import BaseMetadata
from socialapps.core.fields import ImageWithThumbsField


class Template(models.Model):
    """A template displays the content of an object.

    **Attributes:**

    name
        The name of the template. This is displayed to the LFC user to select
        a template. Also used by developers to register a template to a content
        type.

    path
        The relative path to the template file according to Django templating
        engine.

    image
        Stores an image preview of template

    """
    name = models.CharField(max_length=50, unique=True)
    path = models.CharField(max_length=100)
    image = ImageWithThumbsField(_(u"Image"), upload_to="uploads",sizes=((128, 128), (256, 256)))
    
    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return self.name

class PortalType(models.Model):
    """Stores all registration relevant information of a registered content
    type.

    **Attributes:**

    type
        The type of the registered content type.

    name
        The name of the registered content type. This is displayed to the LFC
        users to add a new content type. Also used by developers for
        registration purposes.

    global_addable
        if set to true instances of the content type can be added to the
        portal.

    subtypes
        Allowed sub types which can be added to instances of the content type.

    templates
        Allowed templates which can be selected for instances of the content
        type.

    default_template
        The default template which is assigned when a instance of the content
        type is created.
    """
    type = models.CharField(_(u"Type"), blank=True, max_length=100, unique=True)
    name = models.CharField(_(u"Name"), blank=True, max_length=100, unique=True)
    global_addable = models.BooleanField(_(u"Global addable"), default=True)
    subtypes = models.ManyToManyField("self", verbose_name=_(u"Allowed sub types"), symmetrical=False, blank=True, null=True)
    templates = models.ManyToManyField("Template", verbose_name=_(u"Templates"), related_name="portal_content_type")
    default_template = models.ForeignKey("Template", verbose_name=_(u"Default template"), blank=True, null=True)

    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return self.name

    def get_subtypes(self):
        """Returns all allowed sub types for the belonging content type.
        """
        return self.subtypes.all()

    def get_templates(self):
        """Returns all allowed templates for the belonging content type.
        """
        return self.templates.all()


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
    portal_type = models.ForeignKey("PortalType", verbose_name=_(u"Portal Type"), blank=True, null=True)
    template    = models.ForeignKey("Template", verbose_name=_(u"Template"), blank=True, null=True)

    def get_absolute_url(self):
        pass
    
    def get_portal_type(self):
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
