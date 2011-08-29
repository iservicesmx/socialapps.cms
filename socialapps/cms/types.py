from socialapps.cms.models import *
from socialapps.cms.registration import PortalTemplate, PortalType, portal_types

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

class FolderTableTemplate(PortalTemplate):
    name = 'folder_table'
    title = 'Folder Table'
    path = 'cms/folder_table.html'
    image = '/static/images/types/folder_table.png'

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
    type = "file"
    title = "File"
    global_addable = False
    subtypes = []
    templates = [FileTemplate,]
    default_template = FileTemplate

class ImageType(PortalType):
    type = "image"
    title = "Image"
    global_addable = False
    subtypes = []
    templates = [ImageTemplate,]
    default_template = ImageTemplate

class PageType(PortalType):
    type = "page"
    title = "Page"
    global_addable = False
    subtypes = [ImageType, FileType,]
    templates = [PageTemplate,]
    default_template = PageTemplate

class MultiPageType(PortalType):
    type = "multipage"
    title = "MultiPage"
    global_addable = False
    subtypes = [PageType, ImageType, FileType]
    templates = [MultiPageTemplate,]
    default_template = MultiPageTemplate

class FolderType(PortalType):
    type = 'folder'
    title = 'Folder'
    global_addable = True
    subtypes = [PageType, MultiPage, FileType, ImageType]
    templates = [FolderTemplate, FolderTableTemplate]
    default_template = FolderTemplate
    
portal_types.registry(File, FileType)
portal_types.registry(Image, ImageType)
portal_types.registry(Page, PageType)
portal_types.registry(MultiPage, MultiPageType)
portal_types.registry(Folder, FolderType)
