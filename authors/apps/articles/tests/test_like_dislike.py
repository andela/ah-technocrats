from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse


class TestArticles(BaseTestCase):
    "class to test liking and disliking of articles"

    def test_like(self):
        """test for liking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.like_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,  {'article': 'You have liked this article'})

    def test_dislike(self):
        """test for liking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.dislike_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'article': "You have disliked this article"})

    def test_like_dislike(self):
        """test for liking then disliking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.like_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.data, {'article': 'You have liked this article'})
        response = self.client.put(self.dislike_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'article': "You have disliked this article"})

    def test_dislike_like(self):
        """test for liking then disliking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.dislike_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'article': "You have disliked this article"})
        response = self.client.put(self.like_article(), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.data, {'article': 'You have liked this article'})

    def test_like_nonexisting_article(self):
        """test for liking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.likearticle_url, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'Error': "Article does not exist"})

    def test_dislike_nonexisting_article(self):
        """test for liking an article"""
        self.user_signup()
        token = self.user_login()
        response = self.client.put(self.dislikearticle_url, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'Error': "Article does not exist"})
