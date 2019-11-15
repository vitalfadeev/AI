from django.urls import path
from communication import views

urlpatterns = [
    path('', views.messages, name='messages'),
    path('inbox/', views.message_inbox_list, name='message_inbox_list'),
    path('sentbox/', views.message_sentbox_list, name='message_sentbox_list'),
    path('new/', views.message_write, name='message_write'),
    path('<int:message_ID>/reply/', views.message_reply, name='message_reply'),
    path('<int:message_ID>/', views.message_detail, name='message_detail'),
    path('<int:message_ID>/delete/', views.message_delete, name='message_delete'),
]