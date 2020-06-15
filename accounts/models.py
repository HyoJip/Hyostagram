from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    profile_photo = models.ImageField(
        upload_to="profile/", blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nickname)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url("accounts:profile", self.slug)
