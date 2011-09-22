from django import forms
from .models import *

class BaseContentEditForm(forms.ModelForm):
    class Meta:
        model = BaseContent
        fields = ("title", "description", "tags", "template", "status")

class FolderEditForm(forms.ModelForm):
    class Meta:
        model = Folder 
        fields = ("title", "description", "tags", "template", "status")
        
class MultiPageEditForm(forms.ModelForm):
    class Meta:
        model = MultiPage 
        fields = ("title", "description", "tags", "template", "status")

class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page 
        fields = ("title", "description", "tags", "template", "status")
        
class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image 
        fields = ("title", "description", "tags", "template", "status", "image")
        
class FileEditForm(forms.ModelForm):
    class Meta:
        model = File 
        fields = ("title", "description", "tags", "template", "status", "file")        