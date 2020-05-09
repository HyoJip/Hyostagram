from .models import Photo, Comment
from django import forms

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ["user", "filtered_image"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]