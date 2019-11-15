from django.shortcuts import render

# Create your views here.
def error403(request):
    return render(request, '403.html')


def error404(request):
    return render(request, '404.html')