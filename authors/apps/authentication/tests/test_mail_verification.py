from django.urls import reverse
from django.core import mail
from rest_framework import status

from authors.apps.authentication.serializers import RegistrationSerializer
from authors.apps.authentication.models import User
from authors.base_file import BaseTestCase

invalid_user_data = {
    'user':{
        "username": "Johndoe",
        "email": "johngmail.com",
        "password": "Johndoe12#"
    }
}
class TestMailVerification(BaseTestCase):
    """ Class for testing mail verifiacation after user signup. """

    def test_mail_sent_successfully(self):
        """ Test that a mail is sent to the user upon successful registration. """
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertIn("Welcome",mail.outbox[0].body)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_received(self):
        """ Test a user reseives mail after successful registration. """
        response = self.client.post(self.register_url, self.register_data, format="json")
        self.assertEqual(response.data['message'], 
        "Thank you for signing up with Authors Haven. Please head over to your email to verify your account.")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activation(self):
        """ Test account activation. """
        # Generate token
        user = RegistrationSerializer(data={
            "username": "Johndoe",
            "email": "john@gmail.com",
            "password": "Johndoe12#"
        })
        validate = user.is_valid(raise_exception=True)
        user = user.save()
        token = user.jwt_token
        activation_url = reverse("authentication:user-activate", 
                kwargs={'token':token})
        response2 = self.client.get(activation_url, kwargs=[token])
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data, "Your account has been confirmed. Proceed to login.")
        
    def test_failed_verification(self):
        """ Test verification fails when user registration does not go through. """
        response = self.client.post(self.register_url, invalid_user_data ,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
    