from django.urls import reverse
from authors.apps.authentication.models import User
from .base_test import BaseTestCase
from rest_framework import status


class TestReports(BaseTestCase):
    def test_report_article_with_valid_data(self):
        response = self.create_report(self.valid_report_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_article_with_invalid_data(self):
        response = self.create_report(self.invalid_report_data)
        resp = str(response.data.get("errors", {}).get("report", ''))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('is not a valid choice' in resp, True)

    def test_get_report_as_not_admin(self):
        article_url, response, token = self.create_article()
        response = self.test_client.post(reverse('articles:report-list'), format='json',
                                         HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_report_as_admin(self):
        User.objects.create_superuser('admin', 'admin@admin.com', 'adminp@ssw0rd')
        login_data = {"user": {
            "email": "admin@admin.com",
            "password": "adminp@ssw0rd"
        }
        }
        admin = self.test_client.post(
            self.login_url,
            login_data,
            format='json')
        admin_token = 'Token ' + admin.data['token']
        response = self.test_client.get(reverse('articles:report-list'), format='json',
                                        HTTP_AUTHORIZATION=admin_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
