from django.conf import settings
from django.db import models
from django.shortcuts import resolve_url
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .mixins import TimeStampedMixin


class Photo(TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="photos")
    image = models.ImageField(upload_to="media/")
    filtered_image = ImageSpecField(source='image', processors=[
                                    ResizeToFill(293, 293)], format="JPEG", options={'quality': 60})
    content = models.TextField(max_length=500, blank=True)
    like = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     self.filtered_image.delete()
    #     super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url("photo:detail", self.id)


class Comment(TimeStampedMixin):
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="comments")
    text = models.TextField(max_length=500)
    like = models.IntegerField(default=0)

    def get_absolute_url(self):
        if self.photo:
            return resolve_url("photo:list")
