from django.contrib import admin

from . import models


admin.site.register(models.ReaGroup)
admin.site.register(models.TelegramUser)
