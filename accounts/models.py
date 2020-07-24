from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    profile_photo = models.ImageField(
        upload_to="profile/", blank=True, default="../static/images/person.png")
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nickname)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url("accounts:profile", self.slug)


class Following(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="friends")

    @classmethod
    def follow(cls, user, another_user):
        obj, is_created = cls.objects.get_or_create(user=user)
        obj.friends.add(another_user)

    @classmethod
    def unfollow(cls, user, another_user):
        obj, is_created = cls.objects.get_or_create(user=user)
        obj.friends.remove(another_user)

    def __str__(self):
        return str(self.user)
