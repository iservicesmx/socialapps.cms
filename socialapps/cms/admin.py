from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from socialapps.cms.models import *

admin.site.register(BaseContent, MPTTModelAdmin)
admin.site.register(Folder, MPTTModelAdmin)
admin.site.register(MultiPage, MPTTModelAdmin)
admin.site.register(Page, MPTTModelAdmin)
admin.site.register(File, MPTTModelAdmin)
admin.site.register(Image, MPTTModelAdmin)