from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


# Create your views here.
@login_required
def Dashboard( request ):
    context = {}
    context.update(locals())
    return render(request, 'dashboard/Dashboard.html', context)


