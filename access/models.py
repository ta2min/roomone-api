import uuid
from django.db import models
from django.utils import timezone
from teams.models import Team, Member


class Access(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    entry_time = models.DateTimeField('入室時間', default=timezone.now)
    leaving_time = models.DateTimeField('退室時間', null=True)


class Webhook(models.Model):

    class WebhookType(models.IntegerChoices):
        SLACK = 1
        TEAMS = 2

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    type = models.IntegerField(choices=WebhookType.choices)
    url = models.URLField('webhookのURL', unique=True)

    def __str__(self):
        return f'{self.team.name} {self.WebhookType(self.type).label}'
