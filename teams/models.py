import uuid

from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
)
from django.db import models


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('チーム名', max_length=30, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField('名前', max_length=20)
    student_number = models.CharField(
        '学籍番号',
        max_length=7,
        validators=[RegexValidator(r'^\d{7}$', '正しい学籍番号を入力してください')]
    )
    join_date = models.DateField('チーム加入日', null=True)

    def __str__(self):
        return f'{ self.student_number } { self.name }'
