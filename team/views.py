from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from team.decorators import user_can_view_team, user_can_edit_team
from team.models import Team
from machine.models import Machine
from team.forms import TeamForm, InviteMemberForm


# Create your views here.
@login_required
def private_list(request):
    current_page = "teams"
    current_subpage = "team-private"
    teams = Team.objects.filter(members=request.user)
    return render(request, 'team/private_list.html',
                        {"current_page": current_page, "teams": teams, "current_subpage":current_subpage})


@login_required
@user_can_view_team
def detail(request, team_ID):
    context = {}
    current_page = "teams"
    team = get_object_or_404(Team, pk=team_ID)

    if request.POST:
        form = InviteMemberForm(request.POST)
        context.update(locals())
        if form.is_valid():
            entry = form.save()

            invited_user = get_object_or_404(User, email=entry.email)
            team.members.add(invited_user)

            try:
                invited_user = get_object_or_404(User, email=entry.email)
                team.members.add(invited_user)
            except:
                print("there is no user with {}".format(entry.email))
                # send email invitation

            return HttpResponseRedirect('/team/%s/' % team_ID)
        else:
            return render(request, 'team/detail.html', context)
    else:
        form = InviteMemberForm()
        context.update(locals())
        return render(request, 'team/detail.html', context)


@login_required
def add(request):
    context = {}
    current_page = "teams"
    current_subpage = "add"
    if request.POST:
        form = TeamForm(request.POST)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.members.add(request.user)
            entry.admins.add(request.user)
            entry.save()
            return HttpResponseRedirect('/team/%s/' % entry.id)
        else:
            return render(request, 'team/add.html', context)
    else:
        form = TeamForm()
        context.update(locals())
        return render(request, 'team/add.html', context)


@login_required
def add_inline(request):
    context = {}
    if request.POST:
        form = TeamForm(request.POST)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.members.add(request.user)
            entry.admins.add(request.user)
            entry.save()
            return HttpResponseRedirect('/team/%s/' % entry.id)
        else:
            return render(request, 'team/add_inline.html', context)
    else:
        form = TeamForm()
        context.update(locals())
        return render(request, 'team/add_inline.html', context)


@login_required
@user_can_edit_team
def edit(request, team_ID):
    context = {}
    current_page = "teams"
    current_subpage = "edit"
    
    team = get_object_or_404(Team, pk=team_ID)

    if request.POST:
        form = TeamForm(request.POST, instance=team)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('/team/%s/' % entry.id)
        else:
            return render(request, 'team/edit.html', context)
    else:
        form = TeamForm(instance=team)
        context.update(locals())
        return render(request, 'team/edit.html', context)


@login_required
@user_can_edit_team
def delete(request, team_ID):
    team = get_object_or_404(Team, pk=team_ID)
    team.delete()
    return HttpResponseRedirect('/team')