from rest_framework import permissions
from teams.models import Member

class IsTeamOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return Member.objects.get(team=obj, account=request.user).owner
        except Member.DoesNotExist:
            return False
