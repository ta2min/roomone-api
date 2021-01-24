from django.contrib import admin

from . import models

admin.site.register(models.Access)
admin.site.register(models.Webhook)
