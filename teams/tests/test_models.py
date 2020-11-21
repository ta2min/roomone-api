from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from django.test import TestCase

from ..models import Member, Team


class MemberTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='TestTeam')
        self.user = get_user_model().objects.create_user(
            username='test_user', email='test@example.com', password='pass'
        )

    def test_right_student_number(self):
        """
        正しい学籍番号のテスト
        """
        student_number = '1234567'
        member = Member(
            name='TestUser', team=self.team, student_number=student_number,
            account=self.user, join_date='2020-01-01'
        )
        member.full_clean()
        member.save()
        self.assertEqual(len(Member.objects.all()), 1)

    def test_student_number_alphabetical_mix(self):
        """
        英字が混ざっているときにvalidationエラーが起きるかテスト
        """
        # Member.objects.create(name='TestUser', team=self.team, student_number='12345678')
        with self.assertRaises(ValidationError):
            student_number = '123456a'
            member = Member(
                name='TestUser', team=self.team, student_number=student_number,
                account=self.user, join_date='2020-01-01'
            )
            member.full_clean()

    def test_student_number_not_enough_lengh(self):
        """
        桁数が少ないときにvalidationエラーが起きるかテスト
        """
        # Member.objects.create(name='TestUser', team=self.team, student_number='12345678')
        with self.assertRaises(ValidationError):
            student_number = '123456'
            member = Member(
                name='TestUser', team=self.team, student_number=student_number,
                account=self.user, join_date='2020-01-01'
            )
            member.full_clean()
