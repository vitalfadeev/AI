from django.urls import path
from machine import views

urlpatterns = [
    path('add/', views.machine_add_step1, name='machine_add_step1'),
]