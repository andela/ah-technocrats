from rest_framework import status
from authors.base_file import BaseTestCase


class TestAuthentication(BaseTestCase):
    """Test class for the authentication"""

    def test_register_user(self):
        """ The test should return status code 201 for success (POST request)"""
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_bad_email(self):
        """Test user signup with invalid email"""
        wrong_data = {'user': {
                                "username": "Jacob",
                                "email": "invalidemail",
                                "password": "Jakejake12#"
                            }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["email"][0] == "This value does not match the required pattern."

    def test_username_with_less_characters(self):
        """Test username with less than five characters"""
        wrong_data = {'user': {
                                "username": "Jaco",
                                "email": "mail@app.com",
                                "password": "Jakejake12#"
                            }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["username"][0] == "Username has to be more than five characters"

    def test_username_with_invalid_character(self):
        """Test username invalid character"""
        wrong_data = {'user': {
                                "username": "Jacob?",
                                "email": "mail@app.com",
                                "password": "Jakejake12#"
                            }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["username"][0] == "Username can only have alphanumerics, " \
                                                         "a hyphen or underscore with no spacing"

    def test_username_with_whitespace(self):
        """Test username with whitespace"""
        wrong_data = {'user': {
            "username": "Jacob Saudi",
            "email": "mail@app.com",
            "password": "Jakejake12#"
        }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["username"][0] == "Username can only have alphanumerics, " \
                                                         "a hyphen or underscore with no spacing"

    def test_registration_with_no_password(self):
        """test registration with no passowrd"""
        data = {'user': {
                        "username": "Jacob",
                        "email": "mail@app.com"
                            }}
        resp = self.client.post(self.register_url, data, format="json")
        self.assertEqual(resp.status_code, 400)
        assert resp.data['errors']["password"][0] == "This field is required."

    def test_password_with_less_characters(self):
        """Test password with less characters"""
        wrong_data = {'user': {
                                "username": "Jaco",
                                "email": "mail@app.com",
                                "password": "j12"
                            }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["password"][0] == 'Password must have a minimum of eight ' \
                                                         'characters at least one letter,one special ' \
                                                         'character and one number'
    def test_password_with_letters_only(self):
        """Test password with letters only"""
        wrong_data = {'user': {
            "username": "Jaco",
            "email": "mail@app.com",
            "password": "salmanyagaka"
        }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["password"][0] == 'Password must have a minimum of eight ' \
                                                         'characters at least one letter,one special ' \
                                                         'character and one number'

    def test_password_with_numbers_only(self):
        """Test password with numbers only"""
        wrong_data = {'user': {
            "username": "Jaco",
            "email": "mail@app.com",
            "password": "12345678"
        }}
        response = self.client.post(self.register_url, wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data['errors']["password"][0] == 'Password must have a minimum of eight ' \
                                                         'characters at least one letter,one special ' \
                                                         'character and one number'

    def test_registration_of_existing_user(self):
        """test registration of an existing user and email"""
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.register_url, self.register_data, format="json")
        assert response.data["errors"]["email"][0] == "Email address exists"
        assert response.data["errors"]["username"][0] == "Username already exists"
