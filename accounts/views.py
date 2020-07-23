import json

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.core import serializers

from .forms import CreateUserForm, UserForm, ProfileForm
from .models import Profile, Following
from photo.models import Photo


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

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile_user = self.get_object()

        context["connection"] = Following.objects.filter(
            user=self.request.user, friends=profile_user)
        try:
            followee = Following.objects.filter(
                user=profile_user).first().friends.count()
        except:
            followee = Following.objects.filter(user=profile_user).count()
        finally:
            context["followee"] = followee
        context["follower"] = Following.objects.filter(
            friends=profile_user).count()
        return context


class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
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
        try:
            current_user = User.objects.get(pk=request.user.pk)
            user_form = UserForm(request.POST, instance=current_user)

            # PROFILE UPDATE
            if hasattr(current_user, "profile"):
                profile = current_user.profile
                profile_form = ProfileForm(
                    request.POST, request.FILES, instance=profile)

            # PROFILE CREATE
            else:
                profile_form = ProfileForm(request.POST, request.FILES)

            # PROFILE CREATE의 경우 USER와 연결이 필요함
            profile = profile_form.save(commit=False)
            profile.user = current_user                 # Profile 모델의 user에 current_user 지정
            profile.slug = request.POST.get('nickname')
            profile.save()

            user_form.save()

            return redirect("accounts:profile", slug=request.user.profile.slug)

        except Exception:
            messages.add_message(request, messages.ERROR, "형식이 올바르지 않습니다.")
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)


class UserLikePhoto(ListView):
    # model = Photo
    template_name = "accounts/photos_user_liked.html"

    def get_queryset(self, **kwargs):
        queryset = Photo.objects.filter(like__id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = User.objects.get(id=self.request.user.id)
        context['profile_user'] = profile_user

        try:
            followee = Following.objects.filter(
                user=profile_user).first().friends.count()
        except:
            followee = Following.objects.filter(user=profile_user).count()
        finally:
            context["followee"] = followee
        context["follower"] = Following.objects.filter(
            friends=profile_user).count()
        return context


def follow(request, slug):
    current_user = request.user
    target = get_object_or_404(User, profile__slug=slug)

    following = Following.objects.filter(user=current_user, friends=target)
    is_following = True if following else False

    follower = Following.objects.filter(friends=target).count()

    # 이미 팔로우가 되어 있는 상태면 언팔로우하고 대상 팔로워 -1
    if is_following:
        Following.unfollow(current_user, target)
        is_following = False
        follower -= 1

    # 팔로우하고 대상 팔로워 +1
    else:
        Following.follow(current_user, target)
        is_following = True
        follower += 1

    context = {'is_following': is_following,
               'follower': follower}

    return HttpResponse(json.dumps(context), content_type="application/json")


class SearchUser(ListView):
    model = User
    template_name = 'partials/search_result.html'

    def get_queryset(self, **kwargs):
        keyword = self.request.GET.get('keyword')
        queryset = User.objects.filter(profile__slug__icontains=keyword)
        return queryset


# def searchUser(request):
#     keyword = request.GET.get("keyword")
#     user_set = User.objects.filter(
#         profile__slug__icontains=keyword).select_related('profile')

#     return HttpResponse(serializers.serialize('json', user_set), content_type="application/json")
