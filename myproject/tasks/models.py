from django.db import models
import uuid
from user.models import CustomUser


class Tasks(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    title = models.CharField(max_length=255, verbose_name="タイトル")
    description = models.TextField(verbose_name="説明")
    due_date = models.DateTimeField(verbose_name="期限日")

    STATUS_CHOICES = [
        ("pending", "未対応"),
        ("in_progress", "進行中"),
        ("completed", "完了"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="未対応",
        verbose_name="ステータス",
    )

    assigned_member = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="担当者",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.title
