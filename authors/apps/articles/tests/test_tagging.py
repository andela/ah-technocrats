from rest_framework import status
from .base_test import BaseTestCase

class TestArticleTagging(BaseTestCase):
    """
    Test class for article tagging.
    """
    def test_successful_tagging_article(self):
        """
        Test method for successful article tagging.
        """
        saved_article = self.create_article()[1]
        self.assertEqual(saved_article.status_code, status.HTTP_201_CREATED)
        self.assertEqual(saved_article.data['title'], self.article_data['article']['title'])
    
    def test_tagging_without_authentication_fails(self):
        """
        Test for tagging without authentication.
        """
        self.user_signup()
        response = self.test_client.post(self.articles_url, self.article_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empty_tag_list_field_is_allowed(self):
        """
        Test that a blank tag list is allowed.
        """
        data = {
            "article": {
                "title": "Hello world",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": []
                }
        }
        self.user_signup()
        token = 'Token ' + self.user_login()
        response = self.test_client.post(self.articles_url, 
                        data, format='json', 
                        HTTP_AUTHORIZATION=token)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_non_list_tagList_data_fails(self):
        """
        Test that non list type of data for tag is not allowed.
        """
        data = {
            "article": {
                "title": "Hello world",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tags": "hello, world"
                }
        }
        self.user_signup()
        token = 'Token ' + self.user_login()
        response = self.test_client.post(self.articles_url, 
                        data, format='json', 
                        HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        