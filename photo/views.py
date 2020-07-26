import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormMixin,
                                       UpdateView)
from django.views.generic.list import ListView

from .forms import CommentForm, PhotoForm
from .mixins import ValidAuthorRequiredMixin
from .models import Comment, Photo


class PhotoList(LoginRequiredMixin, FormMixin, ListView):
    model = Photo
    paginate_by = 2
    form_class = CommentForm

    def get_queryset(self, **kwargs):
        try:
            followed_user = [
                i for i in self.request.user.following.friends.all()]
            followed_user.append(self.request.user)
            queryset = Photo.objects.filter(user__in=followed_user).prefetch_related(
                'comments__user').select_related('user').prefetch_related('like').order_by('-created_at')
            return queryset
        except Exception:
            return super(PhotoList, self).get_queryset(**kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class PhotoAllList(LoginRequiredMixin, FormMixin, ListView):
    model = Photo
    paginate_by = 2
    form_class = CommentForm

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).prefetch_related(
            'comments__user').select_related('user').prefetch_related('like').order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class PhotoDetail(DetailView, FormMixin):
    model = Photo
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class PhotoCreate(LoginRequiredMixin, CreateView):
    form_class = PhotoForm
    template_name = "photo/photo_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoUpdate(ValidAuthorRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm


class PhotoDelete(ValidAuthorRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:list')


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)

        comment.user = self.request.user

        comment.photo = get_object_or_404(
            Photo, pk=self.kwargs.get('photo_pk'))
        comment.save()
        return HttpResponseRedirect(self.request.POST.get('next', '/'))


class CommentCreateAjaxView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = "comment/comment_container.html"

    def form_valid(self, form):
        comment = form.save(commit=False)

        comment.user = self.request.user

        comment.photo = get_object_or_404(
            Photo, pk=self.kwargs.get("pk"))

        comment.save()

        context = {
            "comments": Comment.objects.select_related("user").filter(photo=comment.photo).order_by("created_at"),
            "pk": Photo.objects.filter(id=comment.photo.id)[0].id,
            "likeClass": "far"
        }   # 템플릿에서 쓰려면 {{}}안에 key 써야함
        # ex) "/detail/{{pk}}" --> "/detail/16"  즉, 중괄호 사라짐

        return render(self.request, "comment/comment_container.html", context)


class CommentDelete(ValidAuthorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):  # form input next에 담겨진 내용을 담아야되기 때문에 변수가 아닌 함수를 오버라이딩
        to = self.request.POST.get('next', '/')
        return to


class CommentUpdate(ValidAuthorRequiredMixin, UpdateView):
    model = Comment
    fields = ['text']

    def get_success_url(self):
        return Comment.objects.get(pk=self.kwargs['pk']).get_absolute_url()


@require_POST
def photo_like(request):
    user = request.user  # 로그인한 유저를 가져온다.
    pk = request.POST.get('pk')
    is_created = True
    photo = get_object_or_404(Photo, pk=pk)  # 해당 오브젝트를 가져온다.

    if photo.like.filter(id=user.id).exists():  # 이미 해당 유저가 likes컬럼에 존재하면
        photo.like.remove(user)  # likes 컬럼에서 해당 유저를 지운다.
        is_created = False
    else:
        photo.like.add(user)
        is_created = True

    context = {'like_count': photo.total_likes,
               'nickname': request.user.profile.nickname,
               'is_created': is_created}

    return HttpResponse(json.dumps(context), content_type="application/json")


@require_POST
def comment_like(request):
    user = request.user  # 로그인한 유저를 가져온다.
    pk = request.POST.get('pk')
    is_created = True
    comment = get_object_or_404(Comment, pk=pk)  # 해당 오브젝트를 가져온다.

    if comment.like.filter(id=user.id).exists():  # 이미 해당 유저가 likes컬럼에 존재하면
        comment.like.remove(user)  # likes 컬럼에서 해당 유저를 지운다.
        is_created = False
    else:
        comment.like.add(user)
        is_created = True

    context = {'is_created': is_created, }

    return HttpResponse(json.dumps(context), content_type="application/json")
