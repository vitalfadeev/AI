from django.db import models
import collections
from django_mysql.models import JSONField


class Server(models.Model):
	Server_ID  				  = models.AutoField(primary_key=True)

	ServerName 				  = models.CharField(max_length=50, unique=True)
	ServerInfoDateTime        = models.DateTimeField(auto_now_add=True, help_text="Date of creation")
	ServerInfoReady           = models.BooleanField(null=True, blank=True, help_text="=1 if ready or =0")
	ServerTypeMachineHardware = JSONField(default=list, blank=True)

	class Meta:
		db_table = 'Server'
		indexes = [
			models.Index( fields=[ 'ServerName' ] ),
		]

	def __str__(self):
		return f'Server_{self.Server_ID}'
