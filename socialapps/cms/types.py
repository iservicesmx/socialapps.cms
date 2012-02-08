from socialapps.cms.models import *
from socialapps.cms.registration import PortalTemplate, PortalType, portal_types
from .forms import *

#=============== Templates Definition ==================

class FileTemplate(PortalTemplate):
    name = 'file'
    title = 'File'
    path = 'cms/file.html'
    image = '/static/images/types/file.png'
    
class ImageTemplate(PortalTemplate):
    name = 'image'
    title = 'Image'
    path = 'cms/image.html'
    image = '/static/images/types/image.png'
    
class FolderTemplate(PortalTemplate):
    name = 'folder'
    title = 'Folder'
    path = 'cms/folder.html'
    image = '/static/images/types/folder.png'
    
class FolderAdminTemplate(PortalTemplate):
    name = 'folder_admin'
    title = 'Folder Admin'
    path = 'cms/folder_admin.html'
    image = '/static/images/types/folder.png'

class FolderTableTemplate(PortalTemplate):
    name = 'folder_table'
    title = 'Folder Table'
    path = 'cms/folder_table.html'
    image = '/static/images/types/folder_table.png'

class FolderContentTemplate(PortalTemplate):
    name = 'folder_content'
    title = 'Folder Content'
    path = 'cms/folder_content.html'
    image = '/static/images/types/folder_content.png'

class PageTemplate(PortalTemplate):
    name = 'page'
    title = 'Page'
    path = 'cms/page.html'
    image = '/static/images/types/page.png'

class MultiPageTemplate(PortalTemplate):
    name = 'multipage'
    title = 'Multi Page'
    path = 'cms/multipage.html'
    image = '/static/images/types/multipage.png'
    
#=============== Types Definition ===================

class FileType(PortalType):
    name = "file"
    title = "File"
    global_addable = False
    subtypes = []
    templates = [FileTemplate,]
    default_template = FileTemplate
    add_form = FileEditForm
    edit_form = FileEditForm    

class ImageType(PortalType):
    name = "image"
    title = "Image"
    global_addable = False
    subtypes = []
    templates = [ImageTemplate,]
    default_template = ImageTemplate
    add_form = ImageEditForm
    edit_form = ImageEditForm    

class PageType(PortalType):
    name = "page"
    title = "Page"
    global_addable = False
    subtypes = [ImageType, FileType,]
    templates = [PageTemplate,]
    default_template = PageTemplate
    add_form = PageEditForm
    edit_form = PageEditForm

class MultiPageType(PortalType):
    name = "multipage"
    title = "MultiPage"
    global_addable = False
    subtypes = [PageType, ImageType, FileType]
    templates = [MultiPageTemplate,]
    default_template = MultiPageTemplate
    add_form = MultiPageEditForm
    edit_form = MultiPageEditForm

class FolderType(PortalType):
    name = 'folder'
    title = 'Folder'
    global_addable = True
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
