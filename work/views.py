from django.shortcuts import render

# Create your views here.
def listworks(request):
    current_page = "work"
    current_subpage = "listworks"
    return render(request, 'work/list_works.html',
                        {"current_page": current_page, "current_subpage": current_subpage})


def viewworks(request):
    current_page = "work"
    current_subpage = "viewworks"
    return render(request, 'work/view_works.html',
                        {"current_page": current_page, "current_subpage": current_subpage})