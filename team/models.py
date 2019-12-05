from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    Team_ID = models.AutoField(primary_key=True)
    TeamName = models.CharField(_('Name'), max_length=200, help_text="The Team are connected to AccessRight, users can have several companies, and companies can have several users, to make this we have a TABLE AccessRight " )
    AdminUser_ID = models.ManyToManyField( settings.AUTH_USER_MODEL, help_text="The user_Id of the Admin of this team, Admin can add/remove users in the team, and rename the team-name"  )

    class Meta:
        db_table = 'Team'
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        indexes = [
            models.Index(fields=['Team_ID']),
            models.Index(fields=['TeamName']),
        ]
