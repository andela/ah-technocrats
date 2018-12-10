from rest_framework import status
from .base_test import BaseTestCase

class TestPostArticle(BaseTestCase):
    def test_successful_article_creation(self):
        # valid data
        saved_article = self.create_article()[1]
        self.assertEqual(saved_article.status_code, status.HTTP_201_CREATED)

    def test_post_using_invalid_data(self):
        self.user_signup()
        token='Token ' + self.user_login()
        response = self.test_client.post(self.articles_url, self.article_invalid_data, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_without_authentication(self):
        self.user_signup()
        response = self.test_client.post(self.articles_url, self.article_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
