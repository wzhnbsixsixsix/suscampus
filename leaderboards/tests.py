from django.test import TestCase
from .models import TreeScore
from accounts.models import CustomUser
from django.urls import reverse
# Create your tests here.

class SetUpTest(TestCase):
    def setUp(self):
        self.leaderboard_url=reverse('leaderboards:leaderboard')
        
        # Creates 20 different users, with different usernames and emails. All have a different score
        self.users = []
        for i in range(20): 
            self.user = CustomUser.objects.create_user(username = f'{i}', email = f'{i}@gmail.com', password = 'TestPassword12345')
            self.users.append(self.user)
            TreeScore.objects.create(user = self.user, score = i)


class LeaderboardTest(SetUpTest):
    # Verifies the user can access the leaderboard page
    def test_user_can_access_leaderboard_page(self):
        self.client.login(username='7', password='TestPassword12345')
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboards/leaderboards.html')

    # Verifies the user can view the top 10 scores on the leader board, and they are correct, and in order
    def test_user_can_view_top_10_scores(self):
        self.client.login(username='7', password='TestPassword12345')
        response = self.client.get(self.leaderboard_url)

        top_10_scores = response.context['top_players']
        scores = TreeScore.objects.order_by('-score')

        self.assertQuerySetEqual(top_10_scores, scores[:10])

    # Verifies the user can see their score and rank on the leaderboard, even when not in the top 10
    def test_user_view_personal_score_and_rank(self):
        self.client.login(username='7', password='TestPassword12345')
        response = self.client.get(self.leaderboard_url)

        user_rank = response.context['user_rank']
        user_score = response.context['user_score']

        self.assertEqual(user_rank, 13)
        self.assertEqual(user_score, 7)