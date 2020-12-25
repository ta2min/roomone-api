from django.utils import timezone
from rest_framework import viewsets
from teams.models import (
    Team,
    Member,
)
from .serializers import TeamSerializer
from .permissions import IsTeamOwner


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes += [IsTeamOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        team = serializer.save()
        Member.objects.create(
            team=team,
            owner=True,
            account=self.request.user,
            name=self.request.user.username,
            join_date=timezone.now(),
        )
