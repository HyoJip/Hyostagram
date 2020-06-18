from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(
        required=False, widget=forms.widgets.FileInput)

    class Meta:
        model = Profile
        fields = ["nickname", "profile_photo"]
