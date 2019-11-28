from django.db import models

# Create your models here.
class Server(models.Model):
    Server_ID  = models.AutoField( primary_key=True )

    ServerName = models.CharField( max_length=255 )
    ServerInfoDateTime = models.DateTimeField(null=True)
    ServerInfoReady = models.BooleanField(default=False)
    ServerTypeMachineHardware = models.TextField(null=True)
