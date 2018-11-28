from rest_framework import status
from .base_test import BaseTestCase

class TestComments(BaseTestCase):
    """ Class for testing comments. """
    
    # test post comment
    def test_comment_creation(self):
        """ Test comment posting. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        self.asserEqual(response.status_code, status.HTTP_201_CREATED)
    
    # test getting comment
    def test_getting_a_comment(self):
        """ Test getting a single comment successfully. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.client.get(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_200_OK)
    
    # test updating comment
    def test_updating_a_comment(self):
        """ Test editing an existing comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.client.put(self.comment_url, self.new_comment_data, format='json')
        self.asserEqual(response2.status_code, status.HTTP_200_OK)
        
    # test deleting comment
    def test_deleting_an_existing_comment(self):
        """ Method for testing deleting an existing comment."""
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.client.delete(self.comment_url)
        self.asserEqual(response2.status_code, status.HTTP_200_OK)


   