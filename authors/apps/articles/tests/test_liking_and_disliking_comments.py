from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse


class TestLikingComments(BaseTestCase):
    "class to test liking and disliking of articles"

    def test_like_comment(self):
        """test for liking a comment"""
        comment_id, token = self.get_comment_id()
        response = self.client.put(self.like_comment_url(comment_id), format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,  {'message': 'You have liked this comment'})

    def test_dislike_comment(self):
        """test for liking a comment"""
        comment_id, token = self.get_comment_id()
        response = self.client.put(self.dislike_comment_url(comment_id) , format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "You have disliked this comment"})

    def test_like_un_like_comment(self):
        """test for liking then disliking a comment"""
        comment_id, token = self.get_comment_id()
        response = self.client.put(self.like_comment_url(comment_id), format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.data, {'message': 'You have liked this comment'})
        response = self.client.put(self.like_comment_url(comment_id), format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "You have unliked this comment"})

    def test_dislike_un_dislike_comment(self):
        """test for liking then unliking a comment"""
        comment_id, token = self.get_comment_id()
        response = self.client.put(self.dislike_comment_url(comment_id), format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "You have disliked this comment"})
        response = self.client.put(self.dislike_comment_url(comment_id), format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.data, {'message': 'This comment has been un-disliked'})

    def test_like_nonexisting_comment(self):
        """test for liking an comment"""
        self.user_signup()
        token = self.user_login()
        non_existing_id = 5 # not existing comment ID
        response = self.client.put(self.like_comment_url(non_existing_id), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': "Comment not found."})

    def test_dislike_nonexisting_comment(self):
        """test for liking an comment"""
        self.user_signup()
        token = self.user_login()
        non_existing_id = 5 # not existing comment ID
        response = self.client.put(self.dislike_comment_url(non_existing_id), format='json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': "Comment not found."})
