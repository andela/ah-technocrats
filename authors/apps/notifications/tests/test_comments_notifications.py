from .base_setup import BaseTest as Base
from rest_framework import status
from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.notifications.models import Notification

class TestNotificationComments(Base):
    def test_successful_get_of_notification(self):
        """
                Tests that a user successfully receiving notifications.
        #         """

        article, slug = self.create_article()
        self.favorite_article(slug)
        self.comment_article(slug)
        response = self.test_client.get(
            reverse('notifications:all_notifications'), HTTP_AUTHORIZATION=self.user_login2())
        resp = str(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('new comment', resp)

