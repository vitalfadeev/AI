from django.db import models
from machine.models import Machine
from server.models import Server
import jsonfield
import collections


class Work(models.Model):
	Work_ID                          = models.AutoField(primary_key=True, help_text="Auto incremential ID")

	CreationDateTime                 = models.DateTimeField(auto_now_add=True, help_text="When This work have been created")
	Machine_ID                       = models.ForeignKey(Machine, related_name="Works", on_delete=models.CASCADE, null=True, blank=True, help_text="To Process this Machine")
	ServerName                       = models.ForeignKey(Server, to_field='ServerName', on_delete=models.CASCADE, null=True, blank=True, help_text="Name of server to do the work")

	IsWorkTraining                   = models.BooleanField(null=True, blank=True, help_text="Always one value is TRUE simultanousely")
	IsWorkSolving                    = models.BooleanField(null=True, blank=True, help_text="Always one value is TRUE simultanousely")

	IsWorkStatusWaitForServerStart   = models.BooleanField(null=True, blank=True, help_text="Always one value is TRUE simultanousely")
	IsWorkStatusServerProcessing     = models.BooleanField(null=True, blank=True, help_text="Always one value is TRUE simultanousely")
	IsWorkStatusServerFinished       = models.BooleanField(null=True, blank=True, help_text="Always one value is TRUE simultanousely")

	DataLineToProcess_FirstLineID    = models.IntegerField(blank=True, null=True, help_text="Because replication is progressive, to check if this line is available before to start processing the work")
	DataLineToProcess_LastLineID     = models.IntegerField(blank=True, null=True, help_text="Because replication is progressive, to check if this line is available before to start processing the work")

	WorkStartedAtDateTime            = models.DateTimeField(auto_now=True)
	WorkStartedByServerName          = models.CharField(max_length=45, default='')
	WorkStartedCountOfLineToProcess  = models.IntegerField(blank=True, null=True)
	WorkDurationEstimationSeconds    = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	WorkFinishedAtDateTime           = models.DateTimeField(null=True, blank=True)
	WorkFinishedByServerName         = models.CharField(max_length=45, default='')
	WorkFinishedCountOfLineToProcess = models.IntegerField(blank=True, null=True)
	WorkFinishedDurationSeconds      = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	Learning_DelayElapsedSeconds     = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	Solving_DelayElapsedSeconds      = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	TextError                        = jsonfield.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, default=[])
	TextWarning                      = jsonfield.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, default=[])

	class Meta:
		db_table = 'Work'
		indexes = [
			models.Index( fields=[ 'Work_ID' ] ),
			models.Index( fields=[ 'CreationDateTime' ] ),
			models.Index( fields=[ 'Machine_ID' ] ),
			models.Index( fields=[ 'ServerName' ] ),
			models.Index( fields=[ 'IsWorkStatusWaitForServerStart' ] ),
			models.Index( fields=[ 'IsWorkStatusServerProcessing' ] ),
			models.Index( fields=[ 'IsWorkStatusServerFinished' ] ),
		]

	# todo: alter this function for returning just warning in the admin page, not the error
	def save(self, *args, **kwargs):
		fields = [
			self.IsWorkTraining,
			self.IsWorkSolving,
			self.IsWorkStatusWaitForServerStart,
			self.IsWorkStatusServerProcessing,
			self.IsWorkStatusServerFinished
		]
		true_number = 0
		for field in fields:
			if field:
				true_number +=1
		if true_number >=2:
			raise NameError(f'only one of these fields can be True: {dir(Work)[4:9]}')

		return super(Work, self).save(*args, **kwargs)


	def __str__(self):
		return f'Work_{self.Work_ID}'
