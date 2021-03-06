from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'apiv1'

routers = routers.DefaultRouter()
routers.register('team', views.TeamViewSet, 'team')
routers.register('members', views.MemberViewSet, 'members')
routers.register('webhook', views.WebhookViewSet, 'webhooks')

urlpatterns = [
    path('', include(routers.urls)),
    path('access/', views.AccessRecordView.as_view(), name='access-record'),
]
