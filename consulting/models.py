from django.db import models

from core import settings
from team.models import Team
from machine.models import Machine


class ConsultingRequest(models.Model):
	class Meta:
		db_table = 'ConsultingRequest'

	ConsultingRequest_ID = models.AutoField(primary_key=True)
	DateTimeCreation     = models.DateTimeField(auto_now=True)
	User_ID              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	Team_ID              = models.ForeignKey(Team, on_delete=models.CASCADE)
	Description          = models.TextField(blank=True)
	Files_1              = models.BinaryField(null=True, blank=True)
	Files_2              = models.BinaryField(null=True, blank=True)
	Files_3              = models.BinaryField(null=True, blank=True)
	Machine_ID           = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE)
	IsStatusRequest      = models.BooleanField(blank=True, null=True)
	IsStatusWaitingConsultantApproval = models.BooleanField(blank=True, null=True)
	WaitingConsultantApprovalDateTime = models.DateTimeField(blank=True, null=True)
	IsStatusContract         = models.BooleanField(blank=True, null=True)
	ContractStartDateTime    = models.DateTimeField(blank=True, null=True)
	IsStatusContractFinished = models.BooleanField(blank=True, null=True)
	IsStatusContractFailed   = models.BooleanField(blank=True, null=True)
	IsStatusContractCancel   = models.BooleanField(blank=True, null=True)
	ContractEndDateTime      = models.DateTimeField(blank=True, null=True)
	Consultant_User_ID       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Consultant_User_ID')
	AmountUSD                = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f'ConsultingRequest_{self.ConsultingRequest_ID}'


class ConsultantApplication(models.Model):
	class Meta:
		db_table = 'ConsultantApplication'

	ConsultingApplication_ID = models.AutoField(primary_key=True)
	User_ID                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ConsultingRequest_ID     = models.ForeignKey(ConsultingRequest, on_delete=models.CASCADE)
	BidUSD = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f'ConsultantApplication_{self.ConsultingApplication_ID}'


class Message(models.Model):
	class Meta:
		db_table = 'Message'
		verbose_name = 'Message'
		verbose_name_plural = 'Messages'

	Message_ID                     = models.AutoField(primary_key=True)
	DateTimeCreation               = models.DateTimeField(auto_now=True)
	User_ID                        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	# TODO: only one destination of Recipient may be present simultaneously
	Recipient_User_ID              = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='Recipient_User_ID')
	Recipient_ConsultingRequest_ID = models.ForeignKey(ConsultingRequest, null=True, blank=True, on_delete=models.CASCADE)
	Recipient_Machine_ID           = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE)

	Message                        = models.TextField(blank=True)
	File                           = models.BinaryField(null=True, blank=True)

	def __str__(self):
		return f'Message_{self.Message_ID}'
