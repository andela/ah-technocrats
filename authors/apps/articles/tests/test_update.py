from rest_framework import status
from .base_test import BaseTestCase

class TestUpdateArticle(BaseTestCase):
    """Test class for article update"""
    def test_successful_article_edit(self):
        """Test method for successful article update"""
        saved_article = self.create_article()
        url = saved_article[0]
        token = saved_article[2]
        response = self.test_client.put(url, self.article_update_data, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Article has been successfully updated.")

    def test_updating_non_existing_article(self):
        """Test for updating of a non existing article"""
        saved = self.create_article()
        token = saved[2]
        url = 'articles/notsaved'
        response = self.test_client.put(url, self.article_update_data, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_by_non_owner(self):
        """Test for updating by a non owner"""
        # User 1
        saved1 = self.create_article()
        article_url = saved1[0]
        # get user2 details
        token = self.create_article_user2()
        response = self.test_client.put(article_url,self.article_update_data, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_with_invalid_data(self):
        """Test update by invalid data"""
        saved_article = self.create_article()
        url = saved_article[0]
        token = saved_article[2]
        response = self.test_client.put(url, self.article_invalid_data2, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
