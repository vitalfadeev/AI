from django.contrib import admin
from machine.models import Column
from machine.models import Machine

# Register your models here.
admin.site.register(Machine)
admin.site.register(Column)