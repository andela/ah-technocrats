from rest_framework import status
from authors.base_file import BaseTestCase
import unittest


@unittest.skip("Skip this class")
@unittest.skip("Not implemented")
class TestAuthentication(BaseTestCase):
    """Test class for the authentication"""


    def test_user_login(self):
        """test login with accurate data"""
        self.client.post(
            self.register_url,
            self.register_data,
            format="json"
        )
        response = self.client.post(
            self.login_url,
            self.login_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_no_data(self):
        """test login with invalid data"""
        data = {
                    "ksksk": "kskskk"
                }
        response = self.client.post(
            self.login_url,
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_with_no_email(self):
        """test login with no email"""

        response = self.client.post(self.login_url, self.login_no_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["email"][0] == "This field may not be blank."

    def test_user_login_with_invalid_password(self):
        """login with invalid passwortd"""

        response = self.client.post(self.login_url, self.login_invalid_pass, format='json')
        self.assertEqual(response.status_code, 400)
        assert response.data['errors']["error"][0] == "A user with this email and password was not found."
