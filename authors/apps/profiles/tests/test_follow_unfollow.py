from django.urls import reverse
from rest_framework import status

from ..models import Profile
from authors.base_file import BaseTestCase


class TestProfileFollowUnfollow(BaseTestCase):
    """
    Handle testing follow and unfollow of authors.
    """
    def authenticated_user(self):
        """
        Get an authenticate user details.
        """
        self.client.post(self.register_url, self.register_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        token = 'Token ' + response.data['token']
        username = response.data['username']
        follow_url = reverse("profiles:follow", kwargs={'username':username})
        followers_url = reverse("profiles:followers", kwargs={'username':username})
        following_url = reverse("profiles:following", kwargs={'username':username})
        return token, follow_url, followers_url, following_url

    def create_user(self):
        """
        Create a user to be used as body data.
        """
        res = self.client.post(self.register_url, self.register_data2, format='json')
        return res.data['data']['username']

    def test_successful_author_following(self):
        """
        Test successfull following of an author.

        Provide valid credentials and data.
        """
        details = self.authenticated_user()
        url = details[1]
        token = details[0]
        author = {"user":self.create_user()}
        response = self.client.post(url, author, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_following_by_unauthenticated_person(self):
        """
        Test following of an author by unauthenticated person.
        """
        details = self.authenticated_user()
        url = details[1]
        token = details[0]
        author = {"user":self.create_user()}
        response = self.client.post(url, author, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_following_a_non_user(self):
        """
        Test following of a non-registered person.
        """
        details = self.authenticated_user()
        url = details[1]
        token = details[0]
        self.create_user()
        response = self.client.post(url, {"user":"MyNameIsNoOne"}, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_unfollowing(self):
        """
        Test successful unfollowing of an author.
        """
        details = self.authenticated_user()
        url = details[1]
        token = details[0]
        author = {"user":self.create_user()}
        response = self.client.delete(url, author, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollowing_by_unauthenticated_person(self):
        """
        Test unauthenticated user unfollowing an author fails.
        """
        details = self.authenticated_user()
        url = details[1]
        token = details[0]
        author = {"user":self.create_user()}
        response = self.client.delete(url, author, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_getting_followers(self):
        """
        Test successful getting of followers.
        """
        details = self.authenticated_user()
        url = details[2]
        token = details[0]
        author = {"user":self.create_user()}
        self.client.post(url, author, format='json', HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_followers_without_authentication(self):
        """
        Test unauthenticated user getting followers fails.
        """
        details = self.authenticated_user()
        url = details[2]
        token = details[0]
        author = {"user":self.create_user()}
        self.client.delete(url, author, format='json', HTTP_AUTHORIZATION=token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_getting_following(self):
        """
        Test successful getting of authors that a user follows.
        """
        details = self.authenticated_user()
        url = details[3]
        token = details[0]
        author = {"user":self.create_user()}
        self.client.delete(url, author, format='json', HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_following_unauthenticated(self):
        """
        Test unauthenticated user getting following fails.
        """
        details = self.authenticated_user()
        url = details[3]
        token = details[0]
        author = {"user":self.create_user()}
        self.client.delete(url, author, format='json', HTTP_AUTHORIZATION=token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
