from django.core import serializers
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from teams.models import (
    Team,
    Member,
)
from access.models import Access
from .serializers import (
    AccessSerializer,
    TeamSerializer,
    MemberSerializer,
)
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


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes += [IsTeamOwner]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        joined_teams = [m.team for m in Member.objects.filter(account=self.request.user)]
        q_teams = [Q(team=team) for team in joined_teams]
        query = Q()
        for q_team in q_teams:
            query |= q_team
        return Member.objects.filter(query).order_by('team')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AccessRecordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = Member.objects.get(
            team=serializer.validated_data.get('team'),
            student_number=serializer.validated_data.get('student_number')
        )
        
        access = Access.objects.filter(member=member).order_by('-entry_time').first()
        if access is None or access.leaving_time:
            access = Access.objects.create(member=member)
        else:
            access.leaving_time = timezone.now()
            access.save()
        return Response(serializers.serialize('json', [access]), status=status.HTTP_201_CREATED)
