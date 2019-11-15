from django.urls import path
from team import views

urlpatterns = [
    path('', views.private_list, name='private_list'),
    path('add/', views.add, name='add'),
    path('<int:team_ID>/', views.detail, name='detail'),
    path('<int:team_ID>/edit/', views.edit, name='edit'),
    path('<int:team_ID>/delete/', views.delete, name='delete'),
    path('add/inline/', views.add_inline, name='add_inline'),
]