from django.urls import path
from machine import views

urlpatterns = [
    path('Machine/Add', views.MachineAdd),
    path('Machine/<int:Machine_ID>/Main', views.MachineMain ),
    path('Machine/<int:Machine_ID>/Describe', views.MachineDescribe ),
    path('Machine/<int:Machine_ID>/datatable-ajax', views.MachineDatatableAjax.as_view() ),

    # path('public/', views.machine_public_list, name='machine_public_list'),
    # path('private/', views.machine_private_list, name='machine_private_list'),
    # path('add/', views.machine_add_step1, name='machine_add_step1'),
    # path('add/<int:machine_ID>/', views.machine_add_step2, name='add_step2'),
    # path('<int:machine_ID>/edit/', views.machine_edit, name='edit'),
    # path('<int:machine_ID>/project/', views.machine_project, name='machine_project'),
    # path('<int:machine_ID>/input/', views.machine_input, name='machine_input'),
    # path('<int:machine_ID>/output/', views.machine_output, name='machine_output'),
    # path('<int:machine_ID>/parameters/', views.machine_nn_parameters, name='machine_nn_parameters'),
    # path('<int:machine_ID>/tensorboard/', views.machine_tensorboard, name='machine_tensorboard'),
    # path('<int:machine_ID>/graph/', views.machine_graph, name='machine_graph'),
    # path('<int:machine_ID>/work/', views.work, name='work'),
    # path('generate/', views.generate, name='generate'),
    # path('<int:machine_ID>/messages/', views.messages, name='messages'),
]