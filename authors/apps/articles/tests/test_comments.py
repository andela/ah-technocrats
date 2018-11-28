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

    def test_comment_creation_with_invalid_data(self):
        """ Test creating a comment using invalid data. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.test_client.post(self.comment_url, 
                self.invalid_comment_data, format='json')
        self.asserEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_commenting_on_non_existing_article(self):
        """ Test commenting on a missing article.  """
        self.user_signup()
        self.user_login()
        response = self.test_client.post(self.comment_url, 
                self.invalid_comment_data, format='json')
        self.asserEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_commenting_by_a_non_user(self):
        """ Test a non-user cannot comment. """
        response = self.test_client.post(self.comment_url,
                self.invalid_comment_data, format='json')
        self.asserEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test getting comment
    def test_getting_a_comment(self):
        """ Test getting a single comment successfully. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.get(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_a_non_existing_comment(self):
        """ Test getting a missing comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.test_client.get(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_400_NOT_FOUND)
    
    def test_getting_comment_from_a_missing_article(self):
        """ Test getting comment from a non-existent article. """
        self.user_signup()
        self.user_login()
        response2 = self.test_client.get(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_getting_all_comments(self):
        """ Test getting all comments to an article. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.get(self.comments_url)
        self.asserEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_all_comments_from_a_missing_article(self):
        """ Test getting all comments from a non-existent article. """
        self.user_signup()
        self.user_login()
        response2 = self.test_client.get(self.comments_url)
        self.asserEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test updating comment
    def test_updating_a_comment(self):
        """ Test editing an existing comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.put(self.comment_url, 
                self.new_comment_data, format='json')
        self.asserEqual(response2.status_code, status.HTTP_200_OK)
    
    def test_updating_with_invalid_data(self):
        """ Test updating comment using invalid data. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.put(self.comment_url, 
                self.invalid_comment_data, format='json')
        self.asserEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_updating_missing_comment(self):
        """ Test updating a non-existent comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.test_client.put(self.comment_url, 
                self.new_comment_data, format='json')
        self.asserEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_logged_in_user_cannot_update(self):
        """ Test a user has to login before updating. """
        self.user_signup()
        self.post_article()
        response = self.test_client.put(self.comment_url, 
                self.new_comment_data, format='json')
        self.asserEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
    # test deleting comment
    def test_deleting_an_existing_comment(self):
        """ Method for testing deleting an existing comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.delete(self.comment_url)
        self.asserEqual(response2.status_code, status.HTTP_200_OK)

    def test_deleting_a_non_existing_comment(self):
        """ Method for testing deleting an existing comment. """
        self.user_signup()
        self.user_login()
        self.post_article()
        response = self.test_client.delete(self.comment_url)
        self.asserEqual(response.status_code, status.HTTP_404_OK)
    
    def test_non_logged_in_user_deletting_comment(self):
        """ Test a user has to login before deleting. """
        self.user_signup()
        self.post_article()
        response = self.post_comment()
        response2 = self.test_client.delete(self.comment_url)
        self.asserEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
   