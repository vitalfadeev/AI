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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from core import views

from rest_framework import routers, serializers, viewsets

from graph.views import GraphViewSet
from machine.views import MachineViewSet

# Routers provide an easy way of automatically determining the URL conf.
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'machine', MachineViewSet)
router.register(r'graph', GraphViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # google, facebook auth
    path('accounts/', include('allauth.urls')),

    # /
    path('', include('dashboard.urls')),

    # batch
    #path('', include('core.batchs.urls')),

    # profile
    # path('profile/', include('user.urls')),

    # team
    # path('team/', include('team.urls')),

    # machine
    path('', include('machine.urls')),

    # work
    # path('work/', include('work.urls')),

    # consulting
    # path('consulting/', include('consulting.urls')),

    # communication
    # path('messages/', include('communication.urls')),

    # consulting
    path('test403/', views.error403, name='403'),
    path('test404/', views.error404, name='404'),

    # front-end
    path( "", views.home, name="home" ),

    # REST
    re_path(r'^api/', include(router.urls)),
]


# for serve static files
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
