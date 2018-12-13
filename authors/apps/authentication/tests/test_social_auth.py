import unittest

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient, APITestCase

@unittest.skip("Skip this class")
@unittest.skip("Not implemented")
class TestSocialAuth(APITestCase):
    """Test class for the socila login via Facebook, twitter and google"""

    def setUp(self):
        """basic setup information for the social auth class"""
        self.oauth_url = reverse('authentication:social_auth')
        self.client = APIClient()
        self.access_token_oauth2 = 'EAAdFry2CZAUEBAIU7cHOJ3MTopaGTPHyzGU5FXaJLLXIewp4n7BKuh\
        D6WglzO84O1ZBh58R7ghsRmx9nMQY0QaTCSa1ljYw9jv2qG7eXyNGXkFXJ5KcgW2gPxxZAStLZB36vF32Op\
        2yLRHaT795lWMLIMLXvmZCPl5Xl4EStZAFxZBNbU3d3J9eoKi9tSYhTOMZD'
        self.access_token_oauth1 = '1496093359-0Eu2CcrnzuUqJLkp5fM4cBkzzrEw3Q1pxTrlUWM'
        self.access_token_secret_oauth1 = 'eOJTDS5zrhLo8iHlv4DdAbsmauPxD2NKPNjAPSICxGteD'

    def test_social_login(self):
        """test successful login with twitter"""
        login_data = {
            "provider": "twitter",
            "access_token": self.access_token_oauth1,
            "access_token_secret": self.access_token_secret_oauth1
        }
        resp = self.client.post(self.oauth_url, data=login_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data["token"])

    def test_login_without_token(self):
        """test login without token"""
        no_token = {
            "provider": "twitter"
        }
        resp = self.client.post(self.oauth_url, data=no_token)
        self.assertTrue(resp.data["errors"])
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_token(self):
        """test login with an invalid token"""
        invalid_token = {
            "provider": "facebook",
            "access_token": 'invalidtokenhere'
        }
        resp = self.client.post(self.oauth_url, data=invalid_token)
        self.assertTrue(resp.data["error"])
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_a_provider(self):
        """test social login without a provider"""
        no_provider = {
            "access_token": 'invalidtokenhere'
        }
        resp = self.client.post(self.oauth_url, data=no_provider)
        self.assertTrue(resp.data["errors"])
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_access_toke_secret(self):
        """test social login missing access token secret for oauth1 such as twitter"""
        no_access_secret = {
            "provider": "twitter",
            "access_token": self.access_token_oauth1
        }
        resp = self.client.post(self.oauth_url, data=no_access_secret)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(resp.data["error"])

    def test_invalid_provider(self):
        """test social login with invalid provider """
        fake_provider = {
            "access_token": self.access_token_oauth2,
            "provider": "fakeprovider"
        }
        resp = self.client.post(self.oauth_url, data=fake_provider)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(resp.data["error"])
        self.assertEqual(resp.data["error"], "The Provider is invalid")
