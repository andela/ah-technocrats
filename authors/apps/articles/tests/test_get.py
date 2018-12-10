from django.urls import reverse
from rest_framework import status
from .base_test import BaseTestCase


url = 'articles/'
class TestGetArticle(BaseTestCase):

    def test_getting_existing_articles(self):
        saved_article = self.create_article()
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_article(self):
        saved = self.create_article()
        article_url = saved[0]
        response = self.test_client.get(article_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existing_article(self):
        article_url = url+"notsaved"
        response = self.test_client.get(article_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
