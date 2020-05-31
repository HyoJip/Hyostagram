from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormMixin,
                                       UpdateView)
from django.views.generic.list import ListView

from .forms import CommentForm, PhotoForm
from .models import Comment, Photo
from .mixins import ValidAuthorRequiredMixin


class PhotoList(LoginRequiredMixin, FormMixin, ListView):
    model = Photo
    paginate_by = 20
    form_class = CommentForm

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).annotate(more_count=Count('comment') -
                                                           1).prefetch_related('comment_set__user').select_related('user').order_by('-created_at')
        return queryset


class PhotoDetail(DetailView):
    model = Photo


class PhotoCreate(LoginRequiredMixin, CreateView):
    form_class = PhotoForm
    template_name = "photo/photo_form.html"

    def form_valid(self, form):

        # def save(self, commit=True):
        #     self.instance = Post(**self.cleaned_data)   # is_vaild() 함수가 수행되고 나면 데이터는 cleaned_data 변수에 사전형객체로 제공됨
        #     if commit:
        #         self.instance.save()
        #     return self.instance

        # def form_valid(self, form):
        # """If the form is valid, save the associated model."""
        # self.object = form.save()
        # """If the form is valid, redirect to the supplied URL."""
        # return HttpResponseRedirect(self.get_success_url())
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoUpdate(ValidAuthorRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm

    def form_invalid(self):
        instance = form.save()
        Photo.objects.filter(photo=instance).delete()
        if self.request.FILES:
            photo = self.request.FILES.get("image")
            Photo(photo=instance, image=photo)
            photo.save()
        return super().form_valid(form)


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


class CommentDelete(ValidAuthorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):  # form input next에 담겨진 내용을 담아야되기 때문에 변수가 아닌 함수를 오버라이딩
        to = self.request.POST.get('next', '/')
        return to


class CommentUpdate(ValidAuthorRequiredMixin, UpdateView):
    model = Comment
    # TODO: 템플릿 작성
    fields = ['text']

    def get_success_url(self):
        return Comment.objects.get(pk=self.kwargs['pk']).get_absolute_url()
