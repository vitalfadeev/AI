from django.http import HttpResponseRedirect
from django.shortcuts import render
from userprofile.forms import EditProfileForm
from team.models import Team
from communication.models import Message

# Create your views here.
def profile_page(request):
    context = {}
    current_page = "profile"
    current_subpage = "profile"

    teams = Team.objects.filter(members=request.user)

    try:
        all_members_accross_teams = teams[0].members.all() # start with the first
        for t in range(teams.count()):
            all_members_accross_teams.union(teams[t].members.all())
    except:
        all_members_accross_teams = []
    
    messages_received = Message.objects.filter(target=request.user)
    messages_sent = Message.objects.filter(created_by=request.user)

    if request.POST:
        form = EditProfileForm(request.POST, instance=request.user)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render(request, 'userprofile/profile_page.html', context)
    else:
        form = EditProfileForm(instance=request.user)
        context.update(locals())
        return render(request, 'userprofile/profile_page.html', context)