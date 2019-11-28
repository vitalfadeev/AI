from django.db import models

# Create your models here.
from django_mysql.models import JSONField


class GlobalLogger(models.Model):
    class Meta:
        db_name = "GlobalLogger"

    Log_ID = models.AutoField(primary_key=True)

    DateTimeCreation = models.DateTimeField(auto_now=True)

    TraceBack = JSONField(null=True, default=list)
    MainModule = models.CharField(max_length=255, null=True)
    MainFunction = models.CharField(max_length=255, null=True)

    Message = models.TextField(null=True)

    HostName = models.CharField(max_length=255, null=True)
    IP = models.IPAddressField(null=True)
