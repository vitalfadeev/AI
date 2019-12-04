from django.contrib import admin

from . import models

admin.site.register(models.ConsultingRequest,)
admin.site.register(models.ConsultantApplication)
admin.site.register(models.Message)
