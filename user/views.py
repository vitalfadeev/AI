from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from user.forms import EditProfileForm
from team.models import Team

from user.serializers import UserSerializer
from rest_framework import generics, viewsets
from rest_framework import mixins
from django.contrib.auth import get_user_model

User = get_user_model()


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
            return render(request, 'user/profile_page.html', context)
    else:
        form = EditProfileForm(instance=request.user)
        context.update(locals())
        return render(request, 'user/profile_page.html', context)



#
# REST
#
class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = ( IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # + graph.render_div()
