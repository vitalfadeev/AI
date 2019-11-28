from django.urls import path
from user import views

urlpatterns = [
    path('', views.profile_page, name='profile_page'),
]
