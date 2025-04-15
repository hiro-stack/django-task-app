from django.shortcuts import render, get_object_or_404, redirect
from .models import Tasks
from .forms import TasksForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


# タスクの一覧をtasksに保存して "tasks:index.htmlに送る"
class TaskIndexView(View):
    def get(self, request):
        user = request.user
        tasks = Tasks.objects.all()
        return render(request, "tasks/tasks_index.html", {"tasks": tasks, "user": user})


# タスクの新規作成
class TasksCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TasksForm()
        return render(request, "tasks/tasks_create.html", {"form": form})

    def post(self, request):
        form = TasksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:tasks_index")
        return render(request, "tasks/tasks_create.html", {"form": form})


# タスクの詳細画面を表示
class TasksDetailView(View):
    def get(self, request, task_id):
        try:
            task = get_object_or_404(Tasks, id=task_id)
        except Http404:
            return render(request, "error_page_handler/404.html", status=404)

        return render(request, "tasks/tasks_detail.html", {"task": task})


# タスクの編集
class TasksUpdateView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        try:
            task = get_object_or_404(Tasks, id=task_id)
        except Http404:
            return render(request, "error_page_handler/404.html", status=404)
        form = TasksForm(instance=task)
        return render(request, "tasks/tasks_update.html", {"form": form})

    def post(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        form = TasksForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("tasks:tasks_detail", task_id=task_id)

        return render(request, "tasks/tasks_update.html", {"form": form})


# タスクの削除
class TasksDeleteView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        try:
            task = get_object_or_404(Tasks, id=task_id)
        except Http404:
            return render(request, "error_page_handler/404.html", status=404)
        return render(request, "tasks/tasks_delete.html", {"task": task})

    def post(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        task.delete()
        return redirect("tasks:tasks_index")


# タスクのステータス変更
class TasksStatusView(LoginRequiredMixin, View):

    def post(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        new_status = request.POST.get("status")
        if new_status:
            task.status = new_status
            task.save()
            return redirect("tasks:tasks_index")


tasks_delete = TasksDeleteView.as_view()
tasks_update = TasksUpdateView.as_view()
tasks_detail = TasksDetailView.as_view()
tasks_index = TaskIndexView.as_view()
tasks_status = TasksStatusView.as_view()
tasks_create = TasksCreateView.as_view()
