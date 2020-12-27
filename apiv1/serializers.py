from rest_framework import serializers
from teams.models import Team, Member


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_at')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'team', 'owner', 'account', 'student_number', 'join_date')
