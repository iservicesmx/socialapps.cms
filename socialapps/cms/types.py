from django.utils.translation import ugettext_lazy as _
from socialapps.cms.models import *
from socialapps.cms.registration import PortalTemplate, PortalType, portal_types
from .forms import *

#=============== Templates Definition ==================

class FileTemplate(PortalTemplate):
    name = 'file'
    title = _('File')
    path = 'cms/file.html'
    image = '/static/images/types/file.png'

class ImageTemplate(PortalTemplate):
    name = 'image'
    title = _('Image')
    path = 'cms/image.html'
    image = '/static/images/types/image.png'

class FolderTemplate(PortalTemplate):
    name = 'folder'
    title = _('Folder')
    path = 'cms/folder.html'
    image = '/static/images/types/folder.png'

class FolderAdminTemplate(PortalTemplate):
    name = 'folder_admin'
    title = _('Folder Admin')
    path = 'cms/folder_admin.html'
    image = '/static/images/types/folder.png'

class FolderTableTemplate(PortalTemplate):
    name = 'folder_table'
    title = _('Folder Table')
    path = 'cms/folder_table.html'
    image = '/static/images/types/folder_table.png'

class FolderContentTemplate(PortalTemplate):
    name = 'folder_content'
    title = _('Folder Content')
    path = 'cms/folder_content.html'
    image = '/static/images/types/folder_content.png'

class PageAdminTemplate(PortalTemplate):
    name = 'page_admin'
    title = _('Page Admin')
    path = 'cms/page_admin.html'
    image = '/static/images/types/page.png'

class PageTemplate(PortalTemplate):
    name = 'page'
    title = _('Page')
    path = 'cms/page.html'
    image = '/static/images/types/page.png'

class MultiPageAdminTemplate(PortalTemplate):
    name = 'multipage_admin'
    title = _('Multi Page Admin')
    path = 'cms/multipage_admin.html'
    image = '/static/images/types/multipage.png'

class MultiPageTemplate(PortalTemplate):
    name = 'multipage'
    title = _('Multi Page')
    path = 'cms/multipage.html'
    image = '/static/images/types/multipage.png'

#=============== Types Definition ===================

class FileType(PortalType):
    name = "file"
    title = _("File")
    global_addable = False
    icon = 'images/icons/32x32/save.png'
    subtypes = []
    templates = [FileTemplate,]
    default_template = FileTemplate
    add_form = FileEditForm
    edit_form = FileEditForm

class ImageType(PortalType):
    name = "image"
    title = _("Image")
    global_addable = False
    icon = 'images/icons/32x32/image.png'
    subtypes = []
    templates = [ImageTemplate,]
    default_template = ImageTemplate
    add_form = ImageEditForm
    edit_form = ImageEditForm

class PageType(PortalType):
    name = "page"
    title = _("Page")
    global_addable = False
    icon = 'images/icons/32x32/page.png'
    subtypes = [ImageType, FileType,]
    templates = [PageTemplate, PageAdminTemplate]
    default_template = PageTemplate
    add_form = PageEditForm
    edit_form = PageEditForm

class MultiPageType(PortalType):
    name = "multipage"
    title = _("MultiPage")
    global_addable = False
    icon = 'images/icons/32x32/multipage.png'
    subtypes = [PageType, ImageType, FileType]
    templates = [MultiPageTemplate, MultiPageAdminTemplate]
    default_template = MultiPageTemplate
    add_form = MultiPageEditForm
    edit_form = MultiPageEditForm

class FolderType(PortalType):
    name = 'folder'
    title = _('Folder')
    global_addable = True
    icon = 'images/icons/32x32/folder.png'
    subtypes = [PageType, MultiPageType, FileType, ImageType]
    templates = [FolderTemplate, FolderAdminTemplate, FolderTableTemplate, FolderContentTemplate]
    default_template = FolderTemplate
    add_form = FolderEditForm
    edit_form = FolderEditForm

portal_types.registry(File, FileType)
portal_types.registry(Image, ImageType)
portal_types.registry(Page, PageType)
portal_types.registry(MultiPage, MultiPageType)
portal_types.registry(Folder, FolderType)
