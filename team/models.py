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


# class InviteMember(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE,
#                             null=True, blank=True)
#     email = models.EmailField()
#
#     modified_date = models.DateTimeField(auto_now=True)
#     created_date = models.DateTimeField(_('Received DateTime'),
#                                         auto_now_add=True)
#
#     def __str__(self):
#         return self.email
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#
#
#     class Meta:
#         verbose_name = _('Invite Member')
#         verbose_name_plural = _('Invite Members')
