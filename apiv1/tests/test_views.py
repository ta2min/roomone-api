import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from accounts.tests.factory import UserFactory
from teams.tests.factory import TeamFactory, MemberFactory
from teams.models import Team, Member


class TeamViewSetsTests(APITestCase):
    """ Test Team View Set"""

    def setUp(self):
        self.user = UserFactory(username='testUser')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_list_200(self):
        """
        list apiの正常系テスト
        """
        TeamFactory.create_batch(3)

        res = self.client.get(reverse('apiv1:team-list'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(res.content)), 3)

    def test_create_and_request_user_as_member(self):
        """
        create apiの正常系テスト
        チームを作成するrequestユーザーがオーナとしてメンバーになるかテスト
        """
        data = {
            "name": "TestTeam"
        }

        res = self.client.post(reverse('apiv1:team-list'), data=data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(Member.objects.all().count(), 1)
        self.assertTrue(Member.objects.get(account=self.user).owner)

    def test_update_201(self):
        """
        update apiの正常系テスト
        """
        team = TeamFactory()
        MemberFactory(team=team, account=self.user, owner=True)

        data = {'name': 'updateTeam'}
        res = self.client.put(
            reverse('apiv1:team-detail', kwargs={'pk': team.id}),
            data=data, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        update_team = Team.objects.get(id=team.id)
        self.assertEqual(update_team.name, 'updateTeam')

    def test_owner_permission(self):
        """
        teamのオーナ以外のuserからのリクエストが403を返すかテスト
        """
        team = TeamFactory()

        res = self.client.get(reverse('apiv1:team-detail', kwargs={'pk': team.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        data = {'name': 'test'}
        res = self.client.put(reverse('apiv1:team-detail', kwargs={'pk': team.id}),
                    data=data, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.delete(reverse('apiv1:team-detail', kwargs={'pk': team.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class MemberViewSetTest(APITestCase):
    """ Test Member View Set"""

    def setUp(self):
        self.user = UserFactory(username='testUser')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_valid_meber_list(self):
        """
        自分が所属しているチームのメンバーのリストを所得できるかテスト
        """
        team1 = TeamFactory(name='team1')
        team2 = TeamFactory(name='team2')
        team3 = TeamFactory(name='team3')

        MemberFactory.create_batch(3, team=team1)
        MemberFactory.create_batch(3, team=team2)
        team3_mebers = MemberFactory.create_batch(3, team=team3)

        MemberFactory(team=team1, account=self.user)
        MemberFactory(team=team2, account=self.user)

        res = self.client.get(reverse('apiv1:members-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        members = json.loads(res.content)
        self.assertEqual(len(members), 8)
        # team3のメンバーが含まれていないことをテスト
        self.assertNotIn(
            [m['id'] for m in members],
            [m.id for m in team3_mebers]
        )

    def test_valid_create_many_members(self):
        """
        複数のメンバーを登録できるかテスト
        """
        team = TeamFactory(name='team')
        MemberFactory(team=team, account=self.user, owner=True)
        data = [
            {
                "name": "member1",
                "team": team.id,
                "owner": False,
                "student_number": "1234567"
            },
            {
                "name": "member2",
                "team": team.id,
                "owner": False,
                "student_number": "0123456"
            }
        ]

        res = self.client.post(reverse('apiv1:members-list'), data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            len(json.loads(res.content)),
            Member.objects.filter(team=team, owner=False).count()
        )
