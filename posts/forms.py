from django import forms
from .models import Post
from .models import Comment
from ckeditor.widgets import CKEditorWidget 

class PostForm(forms.ModelForm):

    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "category",
            "tags",
            "status"
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]