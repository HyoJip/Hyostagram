from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo, Comment
from .forms import PhotoForm, CommentForm
from django.db.models import Count

class PhotoList(ListView):
    model = Photo

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).annotate(more_count=Count('comment')-1)
        return queryset

class PhotoDetail(DetailView):
    model = Photo

class PhotoCreate(LoginRequiredMixin, CreateView):
    form_class = PhotoForm
    template_name = "photo/photo_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)