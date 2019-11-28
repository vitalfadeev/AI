from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from graph.views import GraphViewSet

router = DefaultRouter()

router.register( 'graph', GraphViewSet )
