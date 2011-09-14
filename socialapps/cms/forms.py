from django import forms

class EditForm(forms.ModelForm):
    title = forms.CharField(max_length = "200")
    description = forms.CharField(widget=forms.Textarea)
