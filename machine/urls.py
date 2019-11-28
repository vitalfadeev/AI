from django.urls import path
from machine import views

urlpatterns = [
    path('Machine/Add', views.MachineAdd),
    path('Machine/<int:Machine_ID>/Main', views.MachineMain ),
    path('Machine/<int:Machine_ID>/Describe', views.MachineDescribe ),
    path('Machine/<int:Machine_ID>/datatable-ajax', views.MachineDatatableAjax.as_view() ),
    path('Machines', views.Machines ),
    path('Machines/datatable-ajax', views.MachinesDatatableAjax.as_view() ),
]