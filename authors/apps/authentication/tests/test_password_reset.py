import datetime
import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from authors.base_file import BaseTestCase


class TestPasswordReset(BaseTestCase):
    # Test class for the password reset feature

    def test_request_password_reset_with_valid_email(self):
        self.client.post(self.register_url, self.register_data, format="json")
        data = {"email": self.register_data['user']['email']}
        response = self.client.post(reverse('authentication:forgot_password'), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset_with_invalid_email(self):
        data = {"email": "email@doesnotexist.com"}
        response = self.client.post(reverse('authentication:forgot_password'), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_password_valid_password(self):
        self.client.post(self.register_url, self.register_data, format="json")
        token = jwt.encode({
            "email": self.register_data['user']['email'],
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm='HS256').decode()
        data = {"password": "password!@1"}
        response = self.client.put(reverse("authentication:change_password", kwargs={'token': token}),
                                    data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_password_invalid_password(self):
        self.client.post(self.register_url, self.register_data, format="json")
        token = jwt.encode({
            "email": self.register_data['user']['email'],
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm='HS256').decode()
        data = {"password": "password"}
        response = self.client.put(reverse("authentication:change_password", kwargs={'token': token}),
                                    data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





