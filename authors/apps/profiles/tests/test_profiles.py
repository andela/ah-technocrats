from authors.base_file import BaseTestCase
from django.urls import reverse
from rest_framework import status
from ..models import Profile

class TestProfile(BaseTestCase):
    """test the user profile"""
    def login_user(self):
        """login the user"""
        response = self.client.post(self.login_url, self.login_data, format='json')
        return response.data['token']
    
    def register_user(self):
        """register a new user"""
        response = self.client.post(self.register_url, self.register_data, format='json')
        return response
        
    def test_model_auto_create_user_profile(self):
        """"test model can create user profile upon successful signup"""
        initial_count = Profile.objects.count()
        self.register_user() # register a new user
        new_count = Profile.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_get_authorized_user_profile(self):
        """test getting registered user profile"""
        self.register_user() # register a new user
        token = self.login_user()
        response = self.client.get(self.user_url, format='json', HTTP_AUTHORIZATION='Token ' +token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        """test updating user profile"""
        self.register_user() # register new user
        token = self.login_user()
        response = self.client.put(
            self.user_url, 
            format='json',
            HTTP_AUTHORIZATION='Token '+token,
            data={
                'user':{
                    'website':'newwebsite.com',
                    'phone':'0721201048'
                }
            }
        )
        self.assertEqual(response.data['message'], 'Update successful')
        self.assertIn('phone',response.data['updated-fields'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_user_profile_by_username(self):
        """test getting user profile by username"""
        self.register_user()
        token = self.login_user()
        response = self.client.get(reverse("profiles:profile", kwargs={
            'username':self.register_data['user']['username'],
        }), format='json', HTTP_AUTHORIZATION='Token '+token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existing_profile(self):
        """get a profile for a non-existing username"""
        self.register_user()
        non_existing_username = 'InvalidUser'
        token = self.login_user()
        response = self.client.get(reverse(
            "profiles:profile",
            kwargs={
                'username': non_existing_username,
            }
        ), format='json', HTTP_AUTHORIZATION='Token '+token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['errors']['detail'], 'Profile Not Found')
        
    def test_get_unauthorized_user_profile(self):
        """test getting the user profile for unauthorized user"""
        response = self.client.get(self.user_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_profile_unauthenticated(self):
        """test updating profile without authorization"""
        self.register_user()
        response = self.client.put(self.user_url,{
            'username':"Updated",
        },format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_profile_authorized(self):
        """test updatating the user profile with authorization"""
        self.register_user()
        token = self.login_user()
        response = self.client.put(self.user_url,
        {
            'user':{
                'username':'test_update'
            }
        }, format='json', HTTP_AUTHORIZATION='Token '+token)
        