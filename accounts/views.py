from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.models import User
from django.views import View

from .forms import CreateUserForm, UserForm, ProfileForm
from .models import Profile


class UserCreate(CreateView):
    template_name = "registration/signup.html"
    form_class = CreateUserForm
    success_url = reverse_lazy('accounts:create_user_done')

    def form_valid(self, form):
        ctx = self.get_context_data()
        profile_form = ctx["profile_form"]

        if profile_form.is_valid() and form.is_valid():
            profile = profile_form.save(commit=False)
            user = form.save(commit=False)
            profile.user = user

            form.save()
            profile_form.save()

            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['user_form'] = CreateUserForm(self.request.POST)
            ctx['profile_form'] = ProfileForm(self.request.POST)
        else:
            ctx['user_form'] = CreateUserForm()
            ctx['profile_form'] = ProfileForm()

        return ctx


class UserRegistered(TemplateView):
    template_name = "registration/signup_done.html"


class ProfileView(DetailView):
    template_name = "accounts/profile.html"
    model = User
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        p_obj = Profile.objects.get(slug=slug)
        d_obj = User.objects.get(profile=p_obj)

        return d_obj


class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name
        })

        if hasattr(user, "profile"):
            profile = user.profile
            profile_form = ProfileForm(initial={
                "nickname": profile.nickname,
                "profile_photo": profile.profile_photo
            })

        else:
            profile_form = ProfileForm()

        return render(request, "accounts/profile_update.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        current_user = User.objects.get(pk=request.user.pk)
        user_form = UserForm(request.POST, instance=current_user)

        if user_form.is_valid():
            user_form.save()

        # PROFILE UPDATE
        if hasattr(current_user, "profile"):
            profile = current_user.profile
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=profile)

        # PROFILE CREATE
        else:
            profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            # PROFILE CREATE의 경우 USER와 연결이 필요함
            profile = profile_form.save(commit=False)
            profile.user = current_user                 # Profile 모델의 user에 current_user 지정
            profile.save()

        return redirect("accounts:profile", slug=request.user.profile.slug)
