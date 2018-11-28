from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase


class BaseTestCase(TestCase):
    """ Base test file for articles and comments. """

    def setUp(self):
        """ Basic configurations for the tests. """

        self.test_client = APIClient()
        #urls
        self.register_url = reverse("authentication:user-signup")
        self.login_url = reverse("authentication:user-login")
        self.articles_url = reverse("articles")
        self.comments_url = reverse("articles:comments")
        self.comment_url = reverse("articles:comment")
        
        self.register_data = {'user': {
                                "username": "nana",
                                "email": "nana@nana.nana",
                                "password": "nana123"
                            }}

        self.login_data = { "user": {
                                "email": "nana@nana.nana",
                                "password": "nana123"
                            }}
        
        self.comment_data = { "comment": {
                            "body": "His name was my name too."
                        }}

        self.article_data = { "article": {
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }}

        self.new_comment_data = { "comment": {
                    "body": "Awesome!!!"
                }}
                
        self.invalid_comment_data = { "comment": {
                    "body": " "
                }}

    def user_signup(self):
        """ Method for registering ba user for testing. """
        res = self.test_client.post(
        self.register_url,
        self.register_data,
        format="json")
        return res
    
    
    def user_login(self):
        """ Method for logging in a user tor testing. """
        res = self.test_client.post(
        self.login_url,
        self.login_data,
        format='json')
        return res

    def post_article(self):
        """ Post an article for testing. """
        res = self.test_client.post(
            self.articles_url,
            self.article_data,
            format='json'
        )
        return res

    def post_comment(self):
        """ Post comment to an article. """
        res = self.test_client.post(
                self.comments_url,
                self.comment_data,
                format='json'
            )
        return res