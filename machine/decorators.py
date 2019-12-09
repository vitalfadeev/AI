from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from machine.models import Machine

def user_can_view_machine(function):
    def wrap(request, *args, **kwargs):
        machine = Machine.objects.get(pk=kwargs['machine_ID'])
        if machine.team:
            parent_team = machine.team
        else:
            # if there is a parent team, being the creator is not
            # important. Creator can be removed from team and her
            # access should be disabled. That is why this feature
            # should work only for independent machines.
            if request.user == machine.created_by:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        
        if request.user in parent_team.members.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_can_edit_machine(function):
    def wrap(request, *args, **kwargs):
        machine = Machine.objects.get(pk=kwargs['machine_ID'])
        if machine.team:
            parent_team = machine.team
        else:
            # if there is a parent team, being the creator is not
            # important. Creator can be removed from team and her
            # access should be disabled. That is why this feature
            # should work only for independent machines.
            if request.user == machine.created_by:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        
        if request.user in parent_team.admins.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def file_import_required( f ):
    @wraps( f )
    def wrapper( request, Machine_ID, *args, **kwds ):
        machine = get_object_or_404( Machine, pk=Machine_ID )
        model = machine.get_machine_data_input_lines_model()


        if machine.is_data_imported():
            return f( request, Machine_ID, *args, **kwds )
        else:
            return HttpResponseRedirect( f"/Machine/{Machine_ID}/Describe" )


    return wrapper
