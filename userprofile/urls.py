from django.urls import path
from userprofile import views

urlpatterns = [
    path('', views.profile_page, name='profile_page'),
]
