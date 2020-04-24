from django import forms
from .models import Post
from django.forms.widgets import TextInput


class NewPostForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder':'Enter title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8','placeholder':'Enter content'}))

    class Meta:
        model = Post

        fields = ['title', 'content']


