from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from team.models import Team
from machine.models import Machine
from consulting.models import ConsultingRequest, ConsultingRequestFile
from consulting.forms import ConsultingRequestForm

# Create your views here.
def all_consulting_requests(request):
    current_page = "consulting"
    current_subpage = "all"
    consulting_requests = ConsultingRequest.objects.all()
    return render(request, 'consulting/all_consulting_requests.html', locals())


@login_required
def consulting_request_new(request):
    context = {}
    current_page = "consulting"
    current_subpage = "new"
    
    if request.POST:
        form = ConsultingRequestForm(request.POST, request.FILES)
        form.fields['team'].queryset = Team.objects.filter(members=request.user)
        form.fields['related_machine'].queryset = Machine.objects.filter(created_by=request.user)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.save()
            files = request.FILES.getlist('files')
            for f in files:
                ConsultingRequestFile.objects.create(
                    consulting_request = entry, 
                    attached_file = f, 
                    created_by = request.user
                )
            return HttpResponseRedirect('/consulting/my/')
        else:
            return render(request, 'consulting/consulting_request_new.html', context)
    else:
        form = ConsultingRequestForm()
        form.fields['team'].queryset = Team.objects.filter(members=request.user)
        form.fields['related_machine'].queryset = Machine.objects.filter(created_by=request.user)
        context.update(locals())
        return render(request, 'consulting/consulting_request_new.html', context)


def consulting_request_my(request):
    current_page = "consulting"
    current_subpage = "my"
    consulting_requests = ConsultingRequest.objects.filter(created_by=request.user)
    return render(request, 'consulting/consulting_request_my.html', locals())


def consulting_request_consultanview(request, consulting_request_ID):
    current_page = "consulting"
    current_subpage = "consulting"
    consulting_request = get_object_or_404(ConsultingRequest, pk=consulting_request_ID)
    return render(request, 'consulting/consulting_request_consultanview.html', locals())


def consulting_request_ownerview(request, consulting_request_ID):
    current_page = "consulting"
    current_subpage = "owner"
    consulting_request = get_object_or_404(ConsultingRequest, pk=consulting_request_ID)
    return render(request, 'consulting/consulting_request_consultanview.html', locals())


def consulting_request_anyoneview(request, consulting_request_ID):
    current_page = "consulting"
    current_subpage = "public"
    consulting_request = get_object_or_404(ConsultingRequest, pk=consulting_request_ID)
    return render(request, 'consulting/consulting_request_consultanview.html', locals())