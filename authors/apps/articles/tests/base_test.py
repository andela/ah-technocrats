from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase


class BaseTestCase(TestCase):
    """ Base test file for articles and comments. """

    def setUp(self):
        """ Basic configurations for the tests. """

        self.client = APIClient()
        #urls
        self.register_url = reverse("authentication:user-signup")
        self.login_url = reverse("authentication:user-login")
        self.comments_url = reverse("articles")
        
        self.register_data = {'user': {
                                        "username": "nana",
                                        "email": "nana@nana.nana",
                                        "password": "nana123"
                                    }}

        self.login_data = { "user": {
                                        "email": "nana@nana.nana",
                                        "password": "nana123"
                                    }}
