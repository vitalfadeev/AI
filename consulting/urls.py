from django.urls import path
from consulting import views

urlpatterns = [
    path('all/', views.all_consulting_requests, name='all'),
    path('<int:consulting_request_ID>/public/', views.consulting_request_anyoneview, name='public'),
    path('<int:consulting_request_ID>/consulting/', views.consulting_request_consultanview, name='consulting'),
    path('<int:consulting_request_ID>/owner/', views.consulting_request_ownerview, name='owner'),
    path('my/', views.consulting_request_my, name='my'),
    path('new/', views.consulting_request_new, name='new'),
]