from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


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
