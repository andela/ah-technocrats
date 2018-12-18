import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestCommentSections(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.token = self.login().get("token", "")
        self.valid_comment_no_range = dict(
            comment=dict(
                body="This is a big comment"
            )
        )
        self.invalid_comment_invalid_range = dict(
            comment=dict(
                body="Something ranged",
                start=10,
                end=1
            )
        )
        self.invalid_comment_no_valid_range = dict(
            comment=dict(
                body="Something good",
                start=-1,
                end=10
            )
        )
        self.invalid_comment_bad_datatype = dict(
            comment=dict(
                body="Something good",
                start="a",
                end=1
            )
        )
        self.invalid_comment_no_start_range = dict(
            comment=dict(
                body="This is a comment",
                end=1
            )
        )

        self.invalid_comment_highlight_out_of_range = dict(
            comment=dict(
                body="Valid comment",
                start=1,
                end=10000
            )
        )
        self.valid_comment_valid_range = dict(
            comment=dict(
                body="Something good",
                start=1,
                end=3
            )
        )
        self.create_article()
        self.slug = "silas-was-good"
        self.url = reverse("articles:list-create-comment", kwargs={
            'article_slug': self.slug,
        })

    def test_can_comment_on_section(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.valid_comment_valid_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data.get("comment", ''), '')

    def test_cannot_comment_out_of_range(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_comment_highlight_out_of_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        bad_text = response.data.get("errors", {}).get('range', '')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Bad selection", bad_text)

    def test_can_comment_without_range(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.valid_comment_no_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data.get("comment", ''), '')

    def test_invalid_comment_bad_datatype(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_comment_bad_datatype),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("errors", {}).get('range', ''),
                         "The start of the highlight must be less than or equal to than the end of highlight")

    def test_no_start_range(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_comment_no_start_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("errors", {}).get('range', ''),
                         "Please provide both the start and the end or non of "
                         "them they must also be greater than 0")

    def test_invalid_range(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_comment_invalid_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("errors", {}).get('range', ''),
                         "The start of the highlight must be less than or equal to than the end of highlight")

    def test_invalid_start(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_comment_no_valid_range),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("errors", {}).get('range', ''),
                         "Please provide both the start and the end or non of them they must also be greater than 0")

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
            title="Silas Was Good",
            description='Something good from someone',
            body='Something from the shitty mess'
        ))
        self.client.post(reverse("articles:articles"), data=json.dumps(article),
                         content_type="application/json", HTTP_AUTHORIZATION='Token ' + self.token)
