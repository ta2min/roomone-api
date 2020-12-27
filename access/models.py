import uuid
from django.db import models
from django.utils import timezone
from teams.models import Member


class Access(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    entry_time = models.DateTimeField('入室時間', default=timezone.now)
    leaving_time = models.DateTimeField('退室時間', null=True)
