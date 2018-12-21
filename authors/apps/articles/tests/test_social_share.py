from django.urls import reverse
from authors.apps.authentication.models import User
from .base_test import BaseTestCase
from rest_framework import status

class TestSocialSharingArticles(BaseTestCase):
    def test_get_fb_share_link(self):
        share_to_facebook, token = self.get_share_endpoint('facebook')
        response = self.test_client.get(share_to_facebook, format='json', HTTP_AUTHORIZATION=token)
        resp = str(response.data)
        self.assertIn('facebook', resp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_twitter_share_link(self):
        share_to_twitter, token = self.get_share_endpoint('twitter')
        response = self.test_client.get(share_to_twitter, format='json', HTTP_AUTHORIZATION=token)
        resp = str(response.data)
        self.assertIn('twitter', resp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_gplus_share_link(self):
        share_to_google, token = self.get_share_endpoint('gplus')
        response = self.test_client.get(share_to_google, format='json', HTTP_AUTHORIZATION=token)
        resp = str(response.data)
        self.assertIn('google', resp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reddit_share_link(self):
        share_to_reddit, token = self.get_share_endpoint('reddit')
        response = self.test_client.get(share_to_reddit, format='json', HTTP_AUTHORIZATION=token)
        resp = str(response.data)
        self.assertIn('reddit', resp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_email_share_link(self):
        share_to_email, token = self.get_share_endpoint('email')
        response = self.test_client.get(share_to_email, format='json', HTTP_AUTHORIZATION=token)
        resp = str(response.data)
        self.assertIn('mailto', resp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
