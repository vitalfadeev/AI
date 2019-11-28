from django.core.exceptions import PermissionDenied
from team.models import Team

def user_can_view_team(function):
    def wrap(request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['team_ID'])
        if request.user in team.admins.all():
            return function(request, *args, **kwargs)
        elif request.user in team.members.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_can_edit_team(function):
    def wrap(request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['team_ID'])
        if request.user in team.admins.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
