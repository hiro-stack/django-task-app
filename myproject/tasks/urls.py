from . import views
from django.urls import path

app_name = "tasks"

urlpatterns = [
    path("", views.tasks_index, name="tasks_index"),
    path("create", views.tasks_create, name="tasks_create"),
    path("<uuid:task_id>", views.tasks_detail, name="tasks_detail"),
    path("<uuid:task_id>/update", views.tasks_update, name="tasks_update"),
    path("<uuid:task_id>/delete", views.tasks_delete, name="tasks_delete"),
    path("<uuid:task_id>/status", views.tasks_status, name="tasks_status"),
]
