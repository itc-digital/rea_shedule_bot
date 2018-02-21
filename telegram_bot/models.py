from django.db import models


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=12, primary_key=True, unique=True)
    group_title = models.CharField(max_length=30)
    faculty_id = models.CharField(max_length=10)
    course_id = models.CharField(max_length=10)
    asp_keys = models.TextField()
