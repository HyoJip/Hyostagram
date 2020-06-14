from datetime import datetime, timedelta

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone


class ValidAuthorRequiredMixin(AccessMixin):
    """상속받은 객체의 author가 운영진이거나 객체의 author가 아니면 403을 반환한다"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 애초에 로그인을 안했으면 거부한다.
            return self.handle_no_permission()
        elif self.get_object().user != request.user and not request.user.is_staff:
            # 상속받은 객체의 author가 현재 user가 아니고 운영진도 아니라면 거부한다.
            raise PermissionDenied
        else:
            return super(ValidAuthorRequiredMixin, self).dispatch(request, *args, **kwargs)


class TimeStampedMixin(models.Model):
    # 생성일시를 저장한다
    created_at = models.DateTimeField(auto_now_add=True)

    # 주의!
    class Meta:
        abstract = True

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
