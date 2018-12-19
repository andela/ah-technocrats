from .base_setup import BaseTest as Base
from rest_framework import status
from django.urls import reverse
from authors.apps.notifications.models import Notification

class TestArticleDeleteUpdateTests(Base):
    def test_successful_get_of_notification(self):
        """
        Tests that a user successfully receiving notifications.
        """
        self.follow_user()
        self.create_article()
        response = self.test_client.get(
            reverse('notifications:all_notifications'), HTTP_AUTHORIZATION=self.user_login2())
        resp = str(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Hello HelloWorld', resp)

    def test_marking_notification_as_read(self):
        """Test marking a notification as read"""
        self.follow_user()
        self.create_article()
        n = Notification.objects.first()
        response = self.test_client.put(reverse("api-notifications:one_notification", kwargs={'pk': n.id}), HTTP_AUTHORIZATION=self.user_login2())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'The notification has been marked as read')

    def test_deletion_of_a_notification(self):
        """Test that a user can delete their notifications"""
        self.follow_user()
        self.create_article()
        n = Notification.objects.first()
        response = self.test_client.delete(reverse("api-notifications:one_notification", kwargs={'pk': n.id}), HTTP_AUTHORIZATION=self.user_login2())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Notification has been successfully deleted.')

    def test_deletion_of_a_notification_by_non_owner(self):
        """Test that a user can delete which is not thiers"""
        self.follow_user()
        self.create_article()
        n = Notification.objects.first()
        response = self.test_client.delete(reverse("api-notifications:one_notification", kwargs={'pk': n.id}), HTTP_AUTHORIZATION=self.user_login1())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You cannot perform this action. Ensure this notification belongs to '
                                                 'you')

    def test_deletion_of_a_non_existing_notification(self):
        """Test that a user can delete notification which does not exist"""
        self.follow_user()
        self.create_article()
        n = Notification.objects.first()
        response = self.test_client.delete(reverse("api-notifications:one_notification", kwargs={'pk': 9}), HTTP_AUTHORIZATION=self.user_login1())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Notification not found')

