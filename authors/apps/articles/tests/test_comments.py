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
        response2 = app.client.get(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_200_OK)
    
    # test updating comment
    # test deleting comment

   