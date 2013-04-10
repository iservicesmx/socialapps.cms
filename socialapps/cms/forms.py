import re
from django import forms
from socialapps.core.widgets import RichTextEditor
from socialapps.core.utils import form_title_validator
from .models import *


class BaseContentEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = BaseContent
        fields = ("title", "description", "tags", "hide")
        widgets = {
            'description' : RichTextEditor,
        }

class FolderEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = Folder 
        fields = ("title", "description", "tags", "pagination", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
        
class MultiPageEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = MultiPage 
        fields = ("title", "description", "tags", "show_toc", "hide")
        widgets = {
            'description' : RichTextEditor,
        }

class PageEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = Page 
        fields = ("title", "description", "text","tags", "hide")
        widgets = {
            'description' : RichTextEditor,
            'text' : RichTextEditor,
        }
        
class ImageEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = Image 
        fields = ("title", "description", "tags", "image", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
        
class FileEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = File 
        fields = ("title", "description", "tags", "file", "hide")
        widgets = {
            'description' : RichTextEditor,
        }

        
class LinkEditForm(forms.ModelForm):
    title = forms.CharField(validators=[form_title_validator])
    class Meta:
        model = Link
        fields = ("title", "description", "url", "frame", "redirect", "tags", "hide")
        widgets = {
            'description' : RichTextEditor,
        }
    