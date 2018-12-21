from django.urls import reverse
from rest_framework import status
from .base_test import BaseTestCase


class TestSearchArticles(BaseTestCase):
    """class to test searching and filtering of articles"""

    def test_search_by_title(self):
        """class to test searching by title"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), data={'title': 'Hello'}, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_author(self):
        """class to test searching by author"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), data={'author': 'JohnDoe'}, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_nonexisting_tag(self):
        """class to test nonexisting tag"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), data={'tag': 'dummydata'}, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code,  status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,  {"message": "Your search has not been found."})

    def test_search_nonexisting_title(self):
        """class to test nonexisting title"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), data={'title': 'dummydata'}, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code,  status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,  {"message": "Your search has not been found."})

    def test_search_no_query(self):
        """class to test no query"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,  {"message": "Missing search query."})

    def test_search_nonexisting_author(self):
        """class to test nonexisting author"""

        self.user_signup()
        token = self.user_login()
        response = self.create_article()
        response = self.client.get(reverse("articles:filter"), data={'author': 'dummydata'}, format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code,  status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,  {"message": "Your search has not been found."})
