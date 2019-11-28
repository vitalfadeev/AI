from django.urls import path
from work import views

urlpatterns = [
    path('list/', views.listworks, name='listworks'),
    path('view/', views.viewworks, name='viewworks'),
]