from django.urls import path, re_path
from machine import views, wsgi_view

urlpatterns = [
    # Machine
    path('Machine/Add', views.MachineAdd),
    path('Machine/<int:Machine_ID>/Main', views.MachineMain ),
    path('Machine/<int:Machine_ID>/Describe', views.MachineDescribe ),
    path('Machine/<int:Machine_ID>/datatable-ajax', views.MachineDatatableAjax.as_view() ),
    path('Machines', views.Machines ),
    path('Machines/datatable-ajax', views.MachinesDatatableAjax.as_view() ),

    # NN
    path( 'Machine/<int:Machine_ID>/NN/Main', views.MachineNNMain ),
    path( 'Machine/<int:Machine_ID>/NN/Parameters', views.MachineNNParameters ),
    path( 'Machine/<int:Machine_ID>/NN/Shape', views.MachineNNShape ),

    # NN TensorBoard
    path( 'Machine/<int:Machine_ID>/NN/Tensorboard', views.MachineNNTensorboard ),
    path( 'Machine/<int:Machine_ID>/NN/Tensorboard-engine', views.MachineNNTensorboardEngine ),
    path( 'Machine/<int:Machine_ID>/NN/tf-interactive-inference-dashboard/<path:ResourceFile>', views.MachineNNTensorboardEngineStatic ),
    path( "Machine/<int:Machine_ID>/NN/data/<path:Resource>", wsgi_view.WsgiView.as_view( application=wsgi_view.tb_wsgi_app ) ),

    # Graph
    path( 'Machine/<int:Machine_ID>/InputGraph', views.MachineInputGraph ),
]