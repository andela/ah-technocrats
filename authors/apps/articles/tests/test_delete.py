from rest_framework import status
from .base_test import BaseTestCase

class TestDeleteArticle(BaseTestCase):
    def test_successful_article_deletion(self):
        saved = self.create_article()
        article_url = saved[0]
        token = saved[2]
        response = self.test_client.delete(article_url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_non_existing(self):
        saved = self.create_article()
        token = saved[2]
        url = 'articles/notsaved'
        response = self.test_client.delete(url,HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_by_non_authenticated(self):
        saved = self.create_article()
        url = saved[0]
        response = self.test_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_by_non_owner(self):
        # User 1
        saved1 = self.create_article()
        article_url = saved1[0]
        # get user2 details
        token = self.create_article_user2()
        response = self.test_client.delete(article_url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)