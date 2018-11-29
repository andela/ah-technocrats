
from rest_framework import status
from authors.base_file import BaseTestCase


class TestAuthentication(BaseTestCase):
    """Test class for the authentication"""


    def test_to_register_a_new_user(self):
        """ The test should return status code 201 for success (POST request)"""
        response = self.client.post(
            self.register_url,
            self.register_data,
            format="json"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_bad_email(self):
        """Test user login with invalid email"""
        wrong_data = {'user': {
                                "username": "Jacob",
                                "email": "invalidemail",
                                "password": "jakejake"
                            }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["email"][0] == "Enter a valid email address."

    def test_registration_with_no_password(self):
        """test registration with no passowrd"""
        data = {'user': {
                                "username": "Jacob",
                                "email": "mail@app.com"
                            }}
        resp = self.client.post(self.register_url, data, format="json")
        self.assertEqual(resp.status_code, 400)
        assert resp.data['errors']["password"][0] == "This field is required."

    def test_registration_of_existing_user(self):
        """test registration of an existing user"""
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data["errors"]["email"][0] == "user with this email already exists."
        assert response.data["errors"]["username"][0] == "user with this username already exists."
