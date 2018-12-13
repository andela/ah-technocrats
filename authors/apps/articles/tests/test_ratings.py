import json

from django.urls import reverse
from rest_framework.test import (APIClient,
                                 APITestCase)
from rest_framework import status


class TestRatings(APITestCase):
    def setUp(self):
        self.token = self.login().get("token", "")
        self.user_test = dict(
            email='silaskenn@gmail.com',
            username='silaskenn',
            password='Password@2019'
        )
        self.REGISTER_URL = reverse("authentication:user-signup")
        self.LOGIN_URL = reverse("authentication:user-login")
        self.BASE_URL = 'http://localhost:8000/api/'
        # self.RATING_URL = self.BASE_URL + "articles/good-father/rate/"
        self.RATING_URL = reverse("articles:rate-article", kwargs={'slug': 'good-father'})
        self.create_article()
        self.client = APIClient()

    def test_cannot_rate_without_token(self):
        content = self.client.post(self.RATING_URL, data={'rating': 4})
        self.assertEqual(content.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_rate_without_rating(self):
        content = self.client.post(self.RATING_URL, data={}, HTTP_AUTHORIZATION='Token '+ self.token)
        self.assertEqual(content.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.data.get('rating'), None)

    def test_cannot_rate_with_bad_range(self):
        content = self.client.post(self.RATING_URL, data={'rating': 8}, HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(content.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.data.get('errors', {}).get('rating', 'message'), 'Specify a valid rating between 1 and 5 inclusive')

    def test_cannot_rate_with_non_numeric(self):
        content = self.client.post(self.RATING_URL, data={'rating': 's0'}, HTTP_AUTHORIZATION='Token '+self.token)
        self.assertEqual(content.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.data.get('errors', {}).get('rating', 'message'), 'Specify a valid rating between 1 and 5 inclusive')

    def test_can_rate_article(self):
        content = self.client.post(self.RATING_URL, data={'rating': 4}, HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(content.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content.data.get('article', {}).get('message', 'message')[-1:-5:-1][::-1], '4/5!')

    def login(self):
        self.register()
        user_test = dict(user=dict(
            email='silaskenn@gmail.com',
            username='silaskenn',
            password='Password@2019'
        ))
        logged = self.client.post(reverse("authentication:user-login"), data=json.dumps(user_test),
                                  content_type="application/json")
        return logged.data

    def register(self):
        user_test = dict(user=dict(
            email='silaskenn@gmail.com',
            username='silaskenn',
            password='Password@2019'
        ))
        self.client.post(reverse("authentication:user-signup"), data=json.dumps(user_test),
                         content_type="application/json")

    def create_article(self):
        article = dict(article=dict(
            title="Good father",
            description='Something good from someone',
            body='Something from the shitty mess'
        ))
        self.client.post(reverse("articles:articles"), data=json.dumps(article),
                         content_type="application/json", HTTP_AUTHORIZATION='Token ' + self.token)
