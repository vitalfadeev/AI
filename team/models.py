from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


# Create your models here.
from user.models import User


class Team(models.Model):
    Team_ID = models.AutoField(primary_key=True)
    TeamName = models.CharField(_('Name'), max_length=200)
    AdminUser_ID = models.ManyToManyField( User )
    # Users = models.ManyToManyRel( User )

    class Meta:
        db_table = 'Team'
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
