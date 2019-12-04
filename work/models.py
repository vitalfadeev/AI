from django.db import models
from machine.models import Machine
from server.models import Server
import jsonfield
import collections


class Work(models.Model):
	class Meta:
		db_table = 'Work'

	Work_ID                          = models.AutoField(primary_key=True)
	Machine_ID                       = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
	ServerName                       = models.ForeignKey(Server, to_field='Server_ID', on_delete=models.CASCADE, null=True, blank=True)

	CreationDateTime                 = models.DateTimeField(auto_now=True)
	IsWorkTraining                   = models.BooleanField(null=True, blank=True)
	IsWorkSolving                    = models.BooleanField(null=True, blank=True)
	IsWorkStatusWaitForServerStart   = models.BooleanField(null=True, blank=True)
	IsWorkStatusServerProcessing     = models.BooleanField(null=True, blank=True)
	IsWorkStatusServerFinished       = models.BooleanField(null=True, blank=True)
	DataLineToProcess_FirstLineID    = models.IntegerField(blank=True, null=True)
	DataLineToProcess_LastLineID     = models.IntegerField(blank=True, null=True)
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
