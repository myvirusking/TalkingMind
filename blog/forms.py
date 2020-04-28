from django import forms
from .models import Post
from django.forms.widgets import TextInput
from users.models import ArticleCategory


class NewPostForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder':'Enter title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8','placeholder':'Enter content'}))
    category = forms.ChoiceField(choices=[(category.id, category.name) for category in ArticleCategory.objects.all()],widget=forms.Select(
        attrs={'class': 'form-control','style':'margin-top:15px;margin-bottom:15px;'}
    ))

    class Meta:
        model = Post
        fields = ['title', 'content','category']

    def clean_category(self):
        category_id = self.cleaned_data['category']
        category_obj = ArticleCategory.objects.get(id = category_id)
        return category_obj