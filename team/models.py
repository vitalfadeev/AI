from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your models here.
class Team(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    admins = models.ManyToManyField(User,
                    related_name='team_admins',
                    verbose_name=_('admins'))
    members = models.ManyToManyField(User,
                    related_name='team_members',
                    verbose_name=_('members'))
    
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Received DateTime'),
                                        auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Group'
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')


class InviteMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                            null=True, blank=True)
    email = models.EmailField()

    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Received DateTime'),
                                        auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _('Invite Member')
        verbose_name_plural = _('Invite Members')
