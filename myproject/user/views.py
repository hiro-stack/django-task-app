from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import SignUpForm, CustomUserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.http import Http404


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != "admin":
            return redirect("tasks:tasks_index")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "registration/user_login.html"


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("tasks:tasks_index")


class UserSignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "registration/user_signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:user_login")
        return render(request, "registration/user_signup.html", {"form": form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "accounts/user_profile.html", {"user": user})


class UserListView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        users = CustomUser.objects.all()
        return render(request, "accounts/users_list.html", {"users": users})


class UsersListCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        form = CustomUserForm()
        return render(request, "accounts/users_create.html", {"form": form})

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:users_list")
        return render(request, "accounts/users_create.html", {"form": form})


class UsersListDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        return render(request, "accounts/users_detail.html", {"user": user})


class UsersListUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
        except Http404:
            # すでに削除された、または存在しないユーザーにアクセスした場合
            return render(request, "error_page_handler/404.html", status=404)
        form = CustomUserForm(instance=user)
        return render(
            request, "accounts/users_update.html", {"form": form, "user": user}
        )

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user:users_list")
        return render(
            request, "accounts/users_update.html", {"form": form, "user": user}
        )


class UsersListDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
        except Http404:
            # すでに削除された、または存在しないユーザーにアクセスした場合
            return render(request, "error_page_handler/404.html", status=404)

        return render(request, "accounts/users_confirm_delete.html", {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return redirect("user:users_list")


login_view = UserLoginView.as_view()
logout_view = UserLogoutView.as_view()
signup_view = UserSignupView.as_view()
profile_view = UserProfileView.as_view()
users_list_view = UserListView.as_view()
users_list_create_view = UsersListCreateView.as_view()
users_list_detail_view = UsersListDetailView.as_view()
users_list_update_view = UsersListUpdateView.as_view()
users_list_delete_view = UsersListDeleteView.as_view()
