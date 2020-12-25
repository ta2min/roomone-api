from django.urls import include, path
from rest_framework import routers
from . import views
from . import permissions

app_name = 'apiv1'

routers = routers.DefaultRouter()
routers.register('team', views.TeamViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]
