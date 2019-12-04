from django.db import models
from machine.models import Machine
from user.models import User


class Billing(models.Model):
	class Meta:
		db_table = 'Billing'
		verbose_name = 'Billing'
		verbose_name_plural = 'Billings'

	Billing_ID            = models.AutoField(primary_key=True)
	Machine_ID            = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
	Machine_Owner_User_ID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Machine_Owner_User_ID')
	Operation_User_ID     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Operation_User_ID')

	Date                                     = models.DateTimeField(auto_now=True)
	OperationIsTraining                      = models.BooleanField(null=True, blank=True)
	CountOfLinesTraining                     = models.IntegerField(blank=True, null=True)
	CountOfTrainingEpoch                     = models.IntegerField(blank=True, null=True)
	TrainingCostMachineOwnerUSD              = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	OperationIsSolving                       = models.BooleanField(null=True, blank=True)
	CountOfLinesSolved                       = models.IntegerField(blank=True, null=True)
	SolvingCostMachineOwnerUSD               = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	OperationIsSolvingAPI                    = models.BooleanField(null=True, blank=True)
	SolvingCostReceivedByMachineOwnerUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	SolvingCostSoldExternalUserUSD           = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	OperationIsMachineCopy                   = models.BooleanField(null=True, blank=True)
	MachineCopyCostReceivedMachineOwnerUSD   = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	MachineCopyCostSoldExternalUserUSD       = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	OperationIsMachineCopyUpdate             = models.BooleanField(null=True, blank=True)
	MachineCopyUpdateCostReceivedMachineOwnerUSD = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	MachineCopyUpdateCostSoldExternalUserUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	OperationIsMachineExport                 = models.BooleanField(null=True, blank=True)
	MachineExportCostReceivedMachineOwnerUSD = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	MachineExportCostSoldExternalUserUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f'Billing_{self.Billing_ID}'