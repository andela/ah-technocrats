from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse


class TestArticles(BaseTestCase):
    "class to test making an article a favorite"

    def test_favorite(self):
        """test for favoriting an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.favorite_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,  {'Success': 'This article is a favourite'})

    def unfavorite_article(self):
        """test for favoriting an article that does not exist"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.unfavorite_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,  {'Success': 'You have removed this article from your favorites'})

    def non_existing_article(self):
        """test for favoriting an article that does not exist"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.favoritearticle_url, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'Success': 'You have removed this article from your favorites'})
