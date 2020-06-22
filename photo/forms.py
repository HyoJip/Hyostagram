from .models import Photo, Comment
from django import forms
from django.utils.translation import gettext_lazy as _


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ["user", "filtered_image", 'like']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "comment_input", "placeholder": "댓글 달기..."})
        }
        labels = {
            "text": _('')
        }
