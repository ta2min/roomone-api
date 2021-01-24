from rest_framework import serializers
from teams.models import Team, Member
from access.models import Access, Webhook


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_at')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'team', 'owner', 'account', 'student_number', 'join_date')


class AccessSerializer(serializers.ModelSerializer):
    team = serializers.UUIDField()
    student_number = serializers.RegexField(regex=r'^\d{7}$')

    class Meta:
        model = Access
        fields = ('id', 'team', 'student_number', 'entry_time', 'leaving_time')
    

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ('id', 'team', 'type', 'url')
