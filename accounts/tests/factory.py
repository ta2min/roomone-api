import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime


tzinfo = pytz.timezone(settings.TIME_ZONE)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        
    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda o: f'{o.username}@example.com')
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(start_dt=timezone.datetime(2020, 1, 1, tzinfo=tzinfo))
