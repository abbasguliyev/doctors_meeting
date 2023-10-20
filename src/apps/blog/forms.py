from django import forms
from ckeditor.widgets import CKEditorWidget
from apps.blog.models import Blog

class BlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input-blog',
        'placeholder': 'Title',
    }))
    content = forms.CharField(widget=CKEditorWidget(config_name="update_doctor"))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-input-file',
        'placeholder': 'image'
    }), required=False)

    class Meta:
        model = Blog
        fields = [
            'title',
            'content',
            'image'
        ]