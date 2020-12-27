from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'apiv1'

routers = routers.DefaultRouter()
routers.register('team', views.TeamViewSet, 'team')
routers.register('members', views.MemberViewSet, 'members')

urlpatterns = [
    path('', include(routers.urls)),
]
