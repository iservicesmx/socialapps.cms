from django import forms

class EditForm(forms.Form):
    name = forms.CharField(max_length = "200")
    description = forms.CharField(widget=forms.Textarea)
