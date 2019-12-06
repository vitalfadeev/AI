from django.conf import settings
from django.db import models
from machine.models import Machine


class Billing(models.Model):
	Billing_ID            = models.AutoField(primary_key=True, help_text="Autogenerated Primary Key")
	Machine_ID            = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True, help_text="Machine performing operation")
	Machine_Owner_User_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='Machine_Owner_User_ID', help_text="Machine=>Owner_User_ID  at the moment when the billing was created")
	Operation_User_ID     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='Operation_User_ID', help_text="User performing the operation")

	Date                                     = models.DateField(auto_now=True, help_text="When operation have been made (Day only)")

	OperationIsTraining                      = models.BooleanField(null=True, blank=True, help_text="The operation logged is a training")
	CountOfLinesTraining                     = models.IntegerField(blank=True, null=True)
	CountOfTrainingEpoch                     = models.IntegerField(blank=True, null=True)
	TrainingCostMachineOwnerUSD              = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Price to be billed to Operation_User_ID")

	OperationIsSolving                       = models.BooleanField(null=True, blank=True, help_text="The operation logged is a solving by the owner")
	CountOfLinesSolved                       = models.IntegerField(blank=True, null=True, help_text="How many lines solved")
	SolvingCostMachineOwnerUSD               = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount to be paid by Operation_User_ID")

	OperationIsSolvingAPI                    = models.BooleanField(null=True, blank=True, help_text="The operation logged is a solving by user not owner, so the owner is paid by user")
	SolvingCostReceivedByMachineOwnerUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount received by Machine_User_ID")
	SolvingCostSoldExternalUserUSD           = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount to be paid by Operation_User_ID ")

	OperationIsMachineCopy                   = models.BooleanField(null=True, blank=True, help_text="The operation was a Machine duplication")
	MachineCopyCostReceivedMachineOwnerUSD   = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount to receive from operation sold to External User _ to received by Machine_User_ID")
	MachineCopyCostSoldExternalUserUSD       = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Price paid by Operation_User_ID")

	OperationIsMachineCopyUpdate             = models.BooleanField(null=True, blank=True, help_text="The operation was a Machine duplicate Update")
	MachineCopyUpdateCostReceivedMachineOwnerUSD = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount to receive from operation sold to External User _ to received by Machine_User_ID")
	MachineCopyUpdateCostSoldExternalUserUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Price paid by Operation_User_ID")

	OperationIsMachineExport                 = models.BooleanField(null=True, blank=True, help_text="The operation was a Machine export to Python")
	MachineExportCostReceivedMachineOwnerUSD = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Amount to receive from operation sold to External User _ to received by Machine_User_ID")
	MachineExportCostSoldExternalUserUSD     = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text="Price paid by Operation_User_ID")

	class Meta:
		db_table = 'Billing'
		verbose_name = 'Billing'
		verbose_name_plural = 'Billings'
		indexes = [
			models.Index( fields=[ 'Billing_ID' ] ),
			models.Index( fields=[ 'Machine_ID' ] ),
			models.Index( fields=[ 'Machine_Owner_User_ID' ] ),
			models.Index( fields=[ 'Operation_User_ID' ] ),
			models.Index( fields=[ 'Date' ] ),
			models.Index( fields=[ 'OperationIsTraining' ] ),
			models.Index( fields=[ 'OperationIsSolving' ] ),
			models.Index( fields=[ 'OperationIsMachineCopy' ] ),
			models.Index( fields=[ 'OperationIsMachineCopyUpdate' ] ),
			models.Index( fields=[ 'OperationIsMachineExport' ] ),
		]

	def __str__(self):
		return f'Billing_{self.Billing_ID}'