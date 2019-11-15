from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from communication.models import Message


# Create your views here.
def messages(request):
    return HttpResponseRedirect('/messages/inbox/')


def message_inbox_list(request):
    current_page = "messages"
    current_subpage = "inbox"
    messages = Message.objects.filter(target=request.user, parent=None)
    return render(request, 'communication/message_private_list.html',
                            {"messages": messages, "current_page": current_page, "current_subpage": current_subpage})


def message_sentbox_list(request):
    current_page = "messages"
    current_subpage = "sentbox"
    messages = Message.objects.filter(created_by=request.user, parent=None)
    return render(request, 'communication/message_sentbox_list.html',
                            {"messages": messages, "current_page": current_page, "current_subpage": current_subpage})


def message_write(request, user_ID=None, message_ID=None):
    current_page = "messages"
    current_subpage = "write"
    if message_ID:
        # message form with a parent
        pass
    else:
        # message without a parent
        pass
    return render(request, 'communication/message_write.html', {"current_page": current_page, "current_subpage": current_subpage})


def message_reply(request, message_ID=None):
    current_page = "messages"
    current_subpage = "reply"
    if message_ID:
        # message form with a parent
        pass
    else:
        # message without a parent
        pass
    return render(request, 'communication/message_write.html', {"current_page": current_page, "current_subpage": current_subpage})


def message_detail(request, message_ID):
    parent_message = get_object_or_404(Message, pk=message_ID)
    return render(request, 'communication/message_detail.html',
                            {"parent_message": parent_message})


def message_delete(request, message_ID):
    message = get_object_or_404(Message, pk=message_ID)
    message.delete()
    return HttpResponseRedirect('/messages/inbox/')