from authors.base_file import BaseTestCase
from django.urls import reverse
from rest_framework import status
from ..models import Profile

class TestProfile(BaseTestCase):
    """test the user profile"""

    def login_user(self):
        """function to login the user"""
        response = self.client.post(self.login_url, self.login_data, format='json')
        return response.data['token']

    def register_user(self):
        """function to register a new user"""
        response = self.client.post(self.register_url, self.register_data, format='json')
        return response

    def test_get_all_authors(self):
        """test getting all authors"""
        self.register_user()
        token = self.login_user()
        response = self.client.get(self.user_author, format='json', HTTP_AUTHORIZATION='Token ' +token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_specific_authors_profile(self):
        """test viewing a specific author's profile"""
        self.register_user()
        token = self.login_user()
        response = self.client.get(reverse("profiles:profile", kwargs={
            'username':self.register_data['user']['username'],
        }), format='json', HTTP_AUTHORIZATION='Token ' +token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
