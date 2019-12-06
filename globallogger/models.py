from django.db import models


class GlobalLogger(models.Model):
	Log_ID 			 = models.AutoField(primary_key=True)

	DateTimeCreation = models.DateTimeField(auto_now_add=True)

	TraceBack        = models.TextField(blank=True, help_text="JSON traceback()")
	MainModule       = models.CharField(max_length=100, help_text="from traceback extract the name of mainmodule")
	MainFunction     = models.CharField(max_length=100, help_text="from traceback extract the name of mainfunction")

	Message          = models.TextField(blank=True, help_text="text parameter")

	HostName         = models.CharField(max_length=45, help_text="hostname of server")
	IP               = models.CharField(max_length=100, help_text="ip of server")

	class Meta:
		db_table = 'GlobalLogger'

		indexes = [
			models.Index( fields=[ 'Log_ID' ] ),
			models.Index( fields=[ 'MainModule' ] ),
			models.Index( fields=[ 'MainFunction' ] ),
			models.Index( fields=[ 'HostName' ] ),
			models.Index( fields=[ 'IP' ] ),
		]
