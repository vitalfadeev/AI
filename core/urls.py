"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from core import views

from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views as rfa_views

from graph.views import GraphViewSet
from machine.admin import AdminDataInputLines, MachineDatatableAjax, MachineDatatableOutputAjax, AdminDataOutputLines
from machine.views import MachineViewSet

# Routers provide an easy way of automatically determining the URL conf.
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'machine', MachineViewSet)
router.register(r'graph', GraphViewSet)

urlpatterns = [
    # Admin
    path('admin/Machine/<int:Machine_ID>/DataInputLines', AdminDataInputLines ),
    path('admin/Machine/<int:Machine_ID>/datatable-ajax', MachineDatatableAjax.as_view() ),
    path('admin/Machine/<int:Machine_ID>/DataOutputLines', AdminDataOutputLines ),
    path('admin/Machine/<int:Machine_ID>/datatable-output-ajax', MachineDatatableOutputAjax.as_view() ),
    path('admin/', admin.site.urls),

    # google, facebook auth
    path('accounts/', include('allauth.urls')),

    # /
    path('', include('dashboard.urls')),

    # machine
    path('', include('machine.urls')),

    # consulting
    path('test403/', views.error403, name='403'),
    path('test404/', views.error404, name='404'),

    # front-end
    path( "", views.home, name="home" ),

    # REST
    re_path(r'^api/', include(router.urls)),
    url( r'^api-token-auth/', rfa_views.obtain_auth_token )
]


# for serve static files
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
