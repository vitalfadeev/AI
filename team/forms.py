from django.forms import ModelForm
from team.models import Team
    # , InviteMember


class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ('admins', 'members', 'created_by',)


# class InviteMemberForm(ModelForm):
#     class Meta:
#         model = InviteMember
#         exclude = ('team',)
