"""File to test user retrival"""
import unittest
from rest_framework import status
from authors.apps.authentication.models import User
from authors.base_file import BaseTestCase

@unittest.skip("Not implemented")
class TestRetrieveUser(BaseTestCase):
    """This class will test user"""

    def test_get_user(self):
        """test getting a user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.user_url, self.login_data, format='json')
        assert response.status_code == 200
        assert response.data["email"] == "jake@jake.jake"
        assert response.data["username"] == "jakejake"

    def test_get_user_without_token(self):
        """test getting user with no token"""
        response = self.client.get(self.user_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(response.data["detail"])
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_get_user_invalid_or_expired_token(self):
        """test getting user with wrong or expired token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "wrongtokenhere")
        response = self.client.get(self.user_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        assert response.data["detail"] == "Invalid token"
