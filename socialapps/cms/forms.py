from django import forms
from .models import *

class BaseContentEditForm(forms.ModelForm):
    class Meta:
        model = BaseContent
        fields = ("title", "description", "tags")

class FolderEditForm(forms.ModelForm):
    class Meta:
        model = Folder 
        fields = ("title", "description", "tags")
        
class MultiPageEditForm(forms.ModelForm):
    class Meta:
        model = MultiPage 
        fields = ("title", "description", "tags")

class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page 
        fields = ("title", "description", "tags")
        
class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image 
        fields = ("title", "description", "tags", "image")
        
class FileEditForm(forms.ModelForm):
    class Meta:
        model = File 
        fields = ("title", "description", "tags", "file")        