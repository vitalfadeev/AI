from django.db import models
import jsonfield
import collections


class Server(models.Model):
	class Meta:
		db_table = 'Server'

	Server_ID  = models.AutoField(primary_key=True)

	ServerName = models.CharField(max_length=50, unique=True)
	ServerInfoDateTime        = models.DateTimeField(auto_now=True)
	ServerInfoReady           = models.BooleanField(null=True, blank=True)
	ServerTypeMachineHardware = jsonfield.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, default=[])

	def __str__(self):
		return f'Server_{self.Server_ID}'
