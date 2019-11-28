from django.contrib import admin
from consulting.models import ConsultingRequest
from consulting.models import ConsultingRequestFile

# Register your models here.
admin.site.register(ConsultingRequest)
admin.site.register(ConsultingRequestFile)