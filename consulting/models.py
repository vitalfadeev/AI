from django.db import models

from core import settings
from team.models import Team
from machine.models import Machine


class ConsultingRequest(models.Model):
	ConsultingRequest_ID = models.AutoField(primary_key=True)

	DateTimeCreation     = models.DateTimeField(auto_now_add=True)

	User_ID              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="creator of the ConsultingRequest")
	Team_ID              = models.ForeignKey(Team, on_delete=models.CASCADE, help_text="Team of the ConsultingRequest or null if there is no team")

	Description          = models.TextField(blank=True)
	Files_1              = models.BinaryField(null=True, blank=True)
	Files_2              = models.BinaryField(null=True, blank=True)
	Files_3              = models.BinaryField(null=True, blank=True)
	Machine_ID           = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE, help_text="link to the machine or null if the request is not related to a machine")

	IsStatusRequest          = models.BooleanField(blank=True, null=True)
	IsStatusWaitingConsultantApproval = models.BooleanField(blank=True, null=True)
	WaitingConsultantApprovalDateTime = models.DateTimeField(blank=True, null=True)
	IsStatusContract         = models.BooleanField(blank=True, null=True)
	ContractStartDateTime    = models.DateTimeField(blank=True, null=True)
	IsStatusContractFinished = models.BooleanField(blank=True, null=True)
	IsStatusContractFailed   = models.BooleanField(blank=True, null=True)
	IsStatusContractCancel   = models.BooleanField(blank=True, null=True)
	ContractEndDateTime      = models.DateTimeField(blank=True, null=True)

	Consultant_User_ID       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Consultant_User_ID')

	AmountUSD                = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)

	class Meta:
		db_table = 'ConsultingRequest'

	def __str__(self):
		return f'ConsultingRequest_{self.ConsultingRequest_ID}'


class ConsultantApplication(models.Model):
	ConsultingApplication_ID = models.AutoField(primary_key=True)
	User_ID                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ConsultingRequest_ID     = models.ForeignKey(ConsultingRequest, on_delete=models.CASCADE)
	BidUSD 					 = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)

	class Meta:
		db_table = 'ConsultantApplication'

	def __str__(self):
		return f'ConsultantApplication_{self.ConsultingApplication_ID}'


class Message(models.Model):
	Message_ID                     = models.AutoField(primary_key=True)

	DateTimeCreation               = models.DateTimeField(auto_now_add=True, help_text="date of message (DateTimeChat)")
	User_ID                        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Message sent by this user")

	# TODO: only one destination of Recipient may be present simultaneously
	Recipient_User_ID              = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='Recipient_User_ID', help_text="Optional (only one destination simultanousely) _ Message sent to this user (only if it is sent to an user)")
	Recipient_ConsultingRequest_ID = models.ForeignKey(ConsultingRequest, null=True, blank=True, on_delete=models.CASCADE, help_text="Optional (only one destination simultanousely) _ Message sent to this consultingRequest (only if the message is part of consultingRequest Discussion)")
	Recipient_Machine_ID           = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE, help_text="Optional (only one destination simultanousely) _ Message sent to this Machine Discussion (only if ity is sent to a machine discussion) ")

	Message                        = models.TextField(blank=True, help_text="Text of the message")
	File                           = models.BinaryField(null=True, blank=True, help_text="One file")

	class Meta:
		db_table = 'Message'
		verbose_name = 'Message'
		verbose_name_plural = 'Messages'

	def __str__(self):
		return f'Message_{self.Message_ID}'
