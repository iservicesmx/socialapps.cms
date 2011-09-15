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
