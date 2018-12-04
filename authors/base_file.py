from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase


class BaseTestCase(TestCase):
    """Base test file to be used by other test files in the project"""
    def setUp(self):
        """Basic configurations of the tests and data for mockups"""
        self.register_data = {'user': {
            "username": "Jacob-Saudi",
            "email": "jake@jake.jake",
            "password": "Ajakejake12#"
        }}

        self.login_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        self.login_no_email = {
            "user": {
                "email": "",
                "password": "jakejake"
            }
        }
        self.login_invalid_pass = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }

        self.client = APIClient()
        self.register_url = reverse("authentication:user-signup")
        self.login_url = reverse("authentication:user-login")

        response = self.client.post(self.login_url, self.login_data, format='json')
        # assert response.data.get("token")
        # self.token = response.data["token"]
        self.token = "dummytokenhere"
        # assert response.status_code == 200
        self.user_url = reverse('authentication:user-retrieve-profile')
