from django.db import models


class GlobalLogger(models.Model):
	class Meta:
		app_label = 'globallogger'
		db_table = 'GlobalLogger'


	Log_ID = models.AutoField(primary_key=True)

	Level            = models.CharField(max_length=10)
	DateTimeCreation = models.DateTimeField(auto_now=True)
	TraceBack        = models.TextField(blank=True)
	MainModule       = models.CharField(max_length=100)
	MainFunction     = models.CharField(max_length=100)
	Message          = models.TextField(blank=True)
	HostName         = models.CharField(max_length=45)
	IP               = models.CharField(max_length=100)
