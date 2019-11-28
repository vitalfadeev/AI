from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from machine.models import Machine
from team.models import Team


# Create your models here.
class ConsultingRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                                verbose_name=_('Team'),
                                null=True, blank=True)

    for_new_machine = models.BooleanField("A New Machine")
    related_machine = models.ForeignKey(Machine, on_delete=models.CASCADE,
                                verbose_name=_('An Existing Machine'),
                                null=True, blank=True)
    request = models.TextField(_('Request'), help_text=_('Please describe your request.'))
    
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Time'),
                                        auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.request
    
    def get_files(self):
        return self.consultingrequestfile_set.all()

    class Meta:
        verbose_name = _('Consulting Request')
        verbose_name_plural = _('Consulting Requests')


class ConsultingRequestFile(models.Model):
    consulting_request = models.ForeignKey(ConsultingRequest, on_delete=models.CASCADE,
                                verbose_name=_('consulting request'),
                                null=True, blank=True)
    
    attached_file = models.FileField(_('file'), null=True, blank=True,
                                upload_to='consultingrequest/%Y-%m-%d/%H-%M')
    
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Time'),
                                        auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return "Attached file for {}".format(self.consulting_request)

    def filename(self):
        return attached_file.path.split('/')[-1]

    class Meta:
        verbose_name = _('Consulting Request File')
        verbose_name_plural = _('Consulting Request Files')