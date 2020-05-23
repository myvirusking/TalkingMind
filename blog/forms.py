from django import forms
from .models import Post, Comment
from django.forms.widgets import TextInput
from users.models import ArticleCategory


class NewPostForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder':'Enter title','style':'margin-top:2px;'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8','placeholder':'Enter content'}))


    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control','style':'margin-top:2px;'}),required=False)

    category = forms.ChoiceField(choices=[(category.id, category.name) for category in ArticleCategory.objects.all()],widget=forms.Select(
        attrs={'class': 'form-control','style':'margin-top:2px;'}
    ))


    class Meta:
        model = Post
        fields = ['title', 'content','category']

    def clean_category(self):
        category_id = self.cleaned_data['category']
        category_obj = ArticleCategory.objects.get(id = category_id)
        return category_obj

class CommentForm(forms.ModelForm):
    commented_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm mr-3 commentInpt','placeholder':'Write a comment...', 'autocomplete':'off'}))

    class Meta:
        model = Comment
        fields = ['commented_text']