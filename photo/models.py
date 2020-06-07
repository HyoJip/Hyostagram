from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.shortcuts import resolve_url
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="photos")
    image = models.ImageField(upload_to="media/")
    filtered_image = ImageSpecField(source='image', processors=[
                                    ResizeToFill(293, 293)], format="JPEG", options={'quality': 60})
    content = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     self.filtered_image.delete()
    #     super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url("photo:detail", self.id)

    def timedelta_string(self):
        # settings에서 Timezone을 'Asia/Seoul'로 변경했을 경우 now()는 로컬타임이지만 DB에 저장된 객체들의 시간은 UTC이다.
        # 차이값을 구하기위해 timezone을 맞춰준다. 이 때 datetime의 timezone이 아닌 django.utils의 timezone을 사용한다.
        delta = datetime.now(tz=timezone.utc) - self.created_at

        if delta < timedelta(minutes=1):
            return str(delta.seconds) + ' 초 전'
        elif delta < timedelta(hours=1):
            return str(int(delta.seconds / 60)) + ' 분 전'
        elif delta < timedelta(days=1):
            return str(int(delta.seconds / 3600)) + ' 시간 전'
        elif delta < timedelta(days=7):
            # 날짜만 따로 빼서 날짜간의 차이를 계산한 후 리턴한다.
            delta = datetime.now(tz=timezone.utc).date() - \
                self.created_at.date()
            return str(delta.days) + ' 일 전'
        else:
            # settings.py에 변경한 로컬 시간대를 기준으로 UTC 시간을 변환하여 리턴한다.

            return "{:%Y년 %m월 %d일}".format(timezone.localtime(self.created_at, timezone.get_current_timezone()))


class Comment(models.Model):
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="comments")
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def get_absolute_url(self):
        if self.photo:
            return resolve_url("photo:list")
