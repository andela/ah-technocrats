import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestTokenGeneration(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = dict(user=dict(
            username="silaskenn",
            email='silaskenn@gmail.com',
            password="SilasK@2019"
        ))
        self.user2 = dict(user=dict(
            email='silaskenn@gmail.com',
            password="SilasK@2019"
        ))
        self.REGISTER_URL = reverse("authentication:user-signup")
        self.LOGIN_URL = reverse("authentication:user-login")

    def test_can_get_signup_token(self):
        content = self.client.post(self.REGISTER_URL,
                                   data=json.dumps(self.user1),
                                   content_type="application/json")
        # decoded = json.loads(content.data)
        token_from_signup = content.data.get("token", "")
        self.assertEqual(content.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(token_from_signup, "")

    def test_can_get_login_token(self):
        posted = self.client.post(self.REGISTER_URL,
                                  data=json.dumps(self.user1),
                                  content_type="application/json")
        content = self.client.post(self.LOGIN_URL,
                                   data=json.dumps(self.user2),
                                   content_type="application/json")
        self.assertEqual(posted.status_code, status.HTTP_201_CREATED)
        print(content.data)
        self.assertEqual(content.status_code, status.HTTP_200_OK)

        token_from_login = content.data.get('token', '')
        self.assertNotEqual(token_from_login, '')
