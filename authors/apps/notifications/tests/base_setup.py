from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        """
        We need a logged in user who follows an author to receive notifications.
        """
        self.test_client = APIClient()
        self.user_data = {
            "user": {
                "username": "JohnDoe",
                "email": "John@andela.com",
                "password": "jaja12ldd34&56"
            }
        }

        self.user_data2 = {
            "user": {
                "username": "JohnDoe2",
                "email": "John2@andela.com",
                "password": "jaja12ldd34&56"
            }
        }

        # urls
        self.register_url = reverse("authentication:user-signup")
        self.login_url = reverse("authentication:user-login")
        self.articles_url = reverse("articles:articles")

        self.token1 = 'Token ' + self.user_login1()

        self.follow_url = reverse(
            'profiles:follow',
            kwargs={"username": "JohnDoe2"})

        self.follow = self.test_client.post(
            self.follow_url,
            HTTP_AUTHORIZATION=self.token1)
        self.article_data = {
            "article": {
                "title": "Hello HelloWorld",
                "description": "Ever wonder how?",
                "body": "You have to believe"
            }
        }
        self.comment_data = {
            "comment": {
                "body": "new comment"
            }
        }
        self.follow_data = {
            "user": "JohnDoe"
        }

    def user_signup(self):
        """ Method for registering ba user for testing. """
        res = self.test_client.post(
            self.register_url,
            self.user_data,
            format="json")
        return res

    def user_signup2(self):
        """ Method for registering ba user for testing. """
        res = self.test_client.post(
            reverse("authentication:user-signup"),
            self.user_data2,
            format="json")
        return res

    def user_login1(self):
        """ Method for logging in a user tor testing. """
        self.user_signup()
        res = self.test_client.post(
            self.login_url,
            self.user_data,
            format='json')
        token = 'Token ' + res.data['token']
        return token

    def user_login2(self):
        """ Method for logging in a user tor testing. """
        self.user_signup2()
        res = self.test_client.post(
            self.login_url,
            self.user_data2,
            format='json')
        token = 'Token ' + res.data['token']
        return token

    def follow_user(self):
        """method to follow user"""
        self.user_login2()
        res = self.test_client.post(
            self.follow_url,
            self.follow_data,
            HTTP_AUTHORIZATION=self.user_login2(),
            format='json')
        return res

    def create_article(self):
        """
            Metrhgod to create articles for the first user
        """
        self.user_signup()
        token = self.user_login1()
        saved_article = self.test_client.post(self.articles_url,
                                              self.article_data, format='json',
                                              HTTP_AUTHORIZATION=token)
        slug = saved_article.data['slug']

        return saved_article, slug

    def favorite_article(self, slug):
        """this methods adds an article to user favorites"""
        favorite_article = reverse("articles:favorite", kwargs={'slug': slug})
        token = self.user_login2()
        res = self.test_client.put(favorite_article,
                                    format='json',
                                   HTTP_AUTHORIZATION=token)

        return res

    def comment_article(self, slug):
        """test comment article"""
        token = self.user_login2()
        comment_url = reverse("articles:list-create-comment", kwargs={'article_slug': slug})
        res = self.test_client.post(comment_url,
                                   self.comment_data, format='json',
                                   HTTP_AUTHORIZATION=token)
        return res, slug
