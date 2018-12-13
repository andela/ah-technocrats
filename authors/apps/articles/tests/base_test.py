from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase


class BaseTestCase(TestCase):
    """ Base test file for articles and comments. """

    def setUp(self):
        """ Basic configurations for the tests. """

        self.test_client = APIClient()
        # urls
        self.register_url = reverse("authentication:user-signup")
        self.login_url = reverse("authentication:user-login")
        self.articles_url = reverse("articles:articles")
        
        self.register_data = {
                            "user":{
                                "username": "JohnDoe",
                                "email": "John@andela.com",
                                "password": "jaja12ldd34&56"
                            }
                            }

        self.register_data2 = {
                            "user":{
                                "username": "JohnDoe2",
                                "email": "John2@andela.com",
                                "password": "jaja12ldd34&56"
                            }
                            }

        self.login_data = {
                            "user":{
                                "email": "John@andela.com",
                                "password": "jaja12ldd34&56"
                            }
                            }

        self.login_data2 = {
                            "user":{
                                "email": "John2@andela.com",
                                "password": "jaja12ldd34&56"
                            }
                            }
        
        self.comment_data = { "comment": {
                            "body": "It's amazing how the universe is mysterious."
                        }}
        self.comment_data2 = {
            "comment":{
                "body":"This is super fun."
            }
        }

        self.article_data = {
                            "article": {
                                "title": "Hello world",
                                "description": "Ever wonder how?",
                                "body": "You have to believe"
                            }
                        }
        self.article_update_data = {
                            "article": {
                                "title": "Hello HelloWorld",
                                "description": "Ever wonder how?",
                                "body": "You have to believe"
                            }
                        }
        self.article_invalid_data = {
                            "article": {
                                "description": "Ever wonder how?",
                                "body": "You have to believe"
                            }
                        }

        self.article_invalid_data2 = {
                            "article": {
                                "description": "",
                                "body": ""
                            }
                        }

        self.new_comment_data = { "comment": {
                    "body": "Awesome!!!"
                }}
                
        self.invalid_comment_data = { "comment": {
                    "body": " "
                }}
        self.reply_data = {
            "reply":{
                "body":"Nice work man"
            }
        }
        self.invalid_reply_data = {
            "reply": {
                "body": ""
            }
        }
        self.reply_data2 = {
            "reply": {
                "body":"This reply was updated"
            }
        }

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
        return res.data['token']
    
    def post_comment(self, comment_data):
        """
        post another comment"""
        response = self.create_article()
        article_slug = response[1].data['slug']
        token = response[2]
        url = reverse("articles:list-create-comment", kwargs={
            'article_slug':article_slug
        })
        response = self.test_client.post(
                url,
                comment_data,
                format='json',
                HTTP_AUTHORIZATION=token
            )
        return response, token, url
    
    def post_reply(self, reply_data, comment_id, url, token):
        return self.test_client.post(
            url+str(comment_id)+'/replies/',
            data=reply_data,
            format='json',
            HTTP_AUTHORIZATION=token
        )
    
    def get_comments(self, token, url):
        """
        get all the comments of an article slug
        """
        return self.test_client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=token
        )
        
    def create_comment(self, token, article_slug):
        """ Post comment to an article. """
        url = reverse("articles:list-create-comment", kwargs={
            'article_slug':article_slug
        })
        response = self.test_client.post(
                url,
                self.comment_data,
                format='json',
                HTTP_AUTHORIZATION=token
            )
        return response
        
    def create_article(self):
        """
            Metrhgod to create articles for the first user
        """
        self.user_signup()
        token = 'Token ' + self.user_login()
        saved_article = self.test_client.post(self.articles_url, 
                        self.article_data, format='json', 
                        HTTP_AUTHORIZATION=token)
        slug = saved_article.data['slug']
        article_url = reverse("articles:get_article", kwargs={'slug':slug})
        
        return article_url, saved_article, token

    def create_article_user2(self):
        """Method to create articles for user 2"""
        self.test_client.post(self.register_url ,self.register_data2, format='json')
        login = self.test_client.post(self.login_url ,self.login_data2, format='json')
        token = 'Token ' + login.data['token']       
        return token
