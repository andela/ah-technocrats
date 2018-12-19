import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestCommentHistory(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.token = self.login().get('token', 'badtoken')
        self.COMMENT_URL = reverse("articles:update-delete-comment", kwargs={
            "article_slug": "good-article",
            "comment_pk": 1
        })
        self.comment = dict(
            comment=dict(
                body="I love playing nothing around"
            )
        )
        self.modified_comment = dict(
            comment=dict(
                body="I love playing guitar around"
            )
        )
        self.create_article()
        self.create_comment()

    def test_cannot_save_no_change(self):
        url = self.COMMENT_URL.replace("/1/",
                                       "/"+str(self.create_comment().get("comment",
                                                                         {}).get('id', 1))+"/")
        self.COMMENT_URL = url
        response = self.client.put(url,
                                   data=json.dumps(self.comment),
                                   content_type="application/json",
                                   HTTP_AUTHORIZATION="Token " + self.token)
        url = self.COMMENT_URL.replace("/1/",
                                       "/"+str(self.create_comment().get("comment",
                                                                         {}).get('id', 1))+"/")
        self.COMMENT_URL = url
        response3 = self.client.get(url)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data.get("previous_versions", [])), 0)

    def test_can_save_edits(self):
        url = self.COMMENT_URL.replace("/1/",
                                       "/"+str(self.create_comment().get("comment",
                                                                         {}).get('id', 1))+"/")
        self.COMMENT_URL = url
        response = self.client.put(url,
                                   data=json.dumps(self.modified_comment),
                                   content_type="application/json",
                                   HTTP_AUTHORIZATION="Token " + self.token)
        response2 = self.client.put(self.COMMENT_URL,
                                    data=json.dumps(self.comment),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        response3 = self.client.get(self.COMMENT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response3.data.get("previous_versions", [])))

    def test_can_get_edits(self):
        url = self.COMMENT_URL.replace("/1/",
                                       "/"+str(self.create_comment().get("comment",
                                                                         {}).get('id', 1))+"/")
        self.COMMENT_URL = url
        self.update_comment()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('previous_versions', ''), '')

    def test_cannot_get_no_edits(self):
        url = self.COMMENT_URL.replace("/1/",
                                       "/"+str(self.create_comment().get("comment",
                                                                         {}).get('id', 1))+"/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('previous_versions', ''), '')

    def create_comment(self):
        data = self.client.post(reverse("articles:list-create-comment", kwargs={
            "article_slug": "good-article"
        }),
                         data=json.dumps(self.comment),
                         content_type="application/json",
                         HTTP_AUTHORIZATION="Token " + self.token)
        return data.data

    def login(self):
        self.register()
        user_test = dict(user=dict(
            email='silaskenn@gmail.com',
            username='silaskenn',
            password='Password@2019'
        ))
        logged = self.client.post(reverse("authentication:user-login"), data=json.dumps(user_test),
                                  content_type="application/json")
        return logged.data

    def register(self):
        user_test = dict(user=dict(
            email='silaskenn@gmail.com',
            username='silaskenn',
            password='Password@2019'
        ))
        self.client.post(reverse("authentication:user-signup"), data=json.dumps(user_test),
                         content_type="application/json")

    def create_article(self):
        article = dict(article=dict(
            title="Good article",
            description='This article is too good for authorshaven',
            body='Sometimes you just have to write code that only you understands'
        ))
        self.client.post(reverse("articles:articles"), data=json.dumps(article),
                         content_type="application/json", HTTP_AUTHORIZATION='Token ' + self.token)

    def update_comment(self):
        res = self.client.put(self.COMMENT_URL,
                              data=json.dumps(self.modified_comment),
                              content_type="application/json",
                              HTTP_AUTHORIZATION="Token " + self.token)
