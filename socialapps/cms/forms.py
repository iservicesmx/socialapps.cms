from django import forms
from .models import *
from socialapps.core.widgets import RichTextEditor

class BaseContentEditForm(forms.ModelForm):
    class Meta:
        model = BaseContent
        fields = ("title", "description", "tags", "hide")
        widgets = {
            'description' : RichTextEditor,
        }

class FolderEditForm(forms.ModelForm):
    class Meta:
        model = Folder 
        fields = ("title", "description", "tags", "pagination", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
        
class MultiPageEditForm(forms.ModelForm):
    class Meta:
        model = MultiPage 
        fields = ("title", "description", "tags", "show_toc", "hide")
        widgets = {
            'description' : RichTextEditor,
        }

class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page 
        fields = ("title", "description", "text","tags", "hide")
        widgets = {
            'description' : RichTextEditor,
            'text' : RichTextEditor,
        }
        
class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image 
        fields = ("title", "description", "tags", "image", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
        
class FileEditForm(forms.ModelForm):
    class Meta:
        model = File 
        fields = ("title", "description", "tags", "file", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
        
class LinkEditForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ("title", "description", "url", "frame", "redirect", "tags", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
    