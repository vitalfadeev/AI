from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                                related_name='message_parent',
                                verbose_name=_('parent'),
                                null=True, blank=True)
    message = models.TextField(_('Message'))
    message_file = models.FileField(_('file'), null=True, blank=True,
                                upload_to='message/%Y-%m-%d/%H-%M')
    
    target = models.ForeignKey(User, related_name='message_target',
                                on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Time'),
                                        auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return "Message from {} to {}".format(self.created_by, self.target)

    def get_replies(self):
        return Message.objects.filter(parent=self).order_by('created_date')

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')