import pytz
from django.conf import settings
from django.utils import timezone
from factory import (
    LazyAttribute,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from accounts.tests.factory import UserFactory
from ..models import Team, Member


tzinfo = pytz.timezone(settings.TIME_ZONE)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = Sequence(lambda n: f'Team{n}')


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    team = SubFactory(TeamFactory)
    owner = False
    account = SubFactory(UserFactory) 
    name = LazyAttribute(lambda o: o.account.username)
    student_number = Sequence(lambda n: str(n).zfill(7))
    join_date = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))
