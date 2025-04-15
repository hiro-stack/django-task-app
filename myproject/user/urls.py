from . import views
from django.urls import path


app_name = "user"

urlpatterns = [
    path("login", views.login_view, name="user_login"),
    path("logout", views.logout_view, name="user_logout"),
    path("signup", views.signup_view, name="user_signup"),
    path("profile", views.profile_view, name="user_profile"),
    path("users/list", views.users_list_view, name="users_list"),
    path(
        "users/create",
        views.users_list_create_view,
        name="users_list_create",
    ),
    path(
        "users/<uuid:user_id>",
        views.users_list_detail_view,
        name="users_list_detail",
    ),
    path(
        "users/<uuid:user_id>/update",
        views.users_list_update_view,
        name="users_list_update",
    ),
    path(
        "users/<uuid:user_id>/delete",
        views.users_list_delete_view,
        name="users_list_delete",
    ),
]
