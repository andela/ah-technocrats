import unittest
from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse


class TestCommentReply(BaseTestCase):
    """
    test replying to article comments
    """

    def test_replying_to_article_comment(self):
        """
        test replying to article's comment
        """
        self.user_signup()
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        comment_id = response1.data['comment']['id']
        response = self.test_client.post(
            url+str(comment_id)+'/replies/',
            data=self.reply_data,
            format='json',
            HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Reply Added Succesfully')

    def test_replying_to_non_existing_article_comment(self):
        """
        test replying to a non existing comment
        """
        self.user_signup()
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        comment_id = 2223 # non exiting comment_id
        response = self.test_client.post(
            url+str(comment_id)+'/replies/',
            data=self.reply_data,
            format='json',
            HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Comment with that ID does not exist')

    def test_replying_to_article_comment_with_invalid_article_slug(self):
        """
        test replying to comment with a non existing article slug
        """
        self.user_signup()
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        comment_id = response1.data['comment']['id']
        url = reverse(
            "articles:list-create-reply",
            kwargs={
                "article_slug": 'non-existing-article-slug',
                'comment_pk': comment_id
            }
        )
        response = self.test_client.post(
            url,
            data=self.reply_data,
            format='json',
            HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article with that slug not found')

    def test_geting_comment_replies(self):
        """
        test getting replies for a given comment"""
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        response = self.post_reply(self.reply_data,comment_id,url, token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # confirm reply creation
        response1 = self.test_client.get(
            url+str(comment_id)+'/replies/',
            format='json',
            HTTP_AUTHORIZATION=token,
        )
        self.assertContains(response1, 'repliesCount')
        self.assertContains(response1, 'replies')
        self.assertIsInstance(response1.data['replies'], list)

    def test_getting_empty_replies(self):
        """
        get replies of comments with no replies
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data) # create a new comment
        comment_id = result.data['comment']['id']
        response = self.test_client.get(
            url+str(comment_id)+'/replies/',
            format='json',
            HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No replies found for this comment')

    def test_getting_replies_without_authentication(self):
        """
        test getting comments without authentication token
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        response = self.post_reply(self.reply_data,comment_id,url, token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # confirm reply creation
        response1 = self.test_client.get( # make request without the authentication token
            url+str(comment_id)+'/replies/',
            format='json',
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_deleting_comment_reply(self):
        """
        test deleting reply of a comment
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        response1 = self.post_reply(self.reply_data,comment_id,url, token)
        reply_id = response1.data['reply']['id']
        response = self.test_client.delete(
            url+str(comment_id)+'/replies/'+str(reply_id)+'/',
            format='json',
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(response.data['message'], 'Reply deleted successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleting_non_existing_reply_id(self):
        """
        test deleting reply with a non existing ID
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        self.post_reply(self.reply_data,comment_id,url, token)
        reply_id = 4455555 # non existing reply ID
        response = self.test_client.delete(
            url+str(comment_id)+'/replies/'+str(reply_id)+'/',
            format='json',
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(response.data['error'], 'Reply with that ID not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_updating_existing_reply(self):
        """
        test editing existing reply ID
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        response1 = self.post_reply(self.reply_data,comment_id,url, token)
        reply_id = response1.data['reply']['id']
        response = self.test_client.put(
            url+str(comment_id)+'/replies/'+str(reply_id)+'/',
            format='json',
            data=self.reply_data2,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Reply Updated Successfully')
        self.assertNotEqual(response.data['reply'], self.reply_data['reply'])

    def test_update_non_existing_reply_id(self):
        """
        test updating non existing reply id
        """
        self.user_signup() # register user
        result, token, url = self.post_comment(self.comment_data)
        comment_id = result.data['comment']['id']
        self.post_reply(self.reply_data,comment_id,url, token)
        reply_id = 4455555 # non existing reply ID
        response = self.test_client.delete(
            url+str(comment_id)+'/replies/'+str(reply_id)+'/',
            format='json',
            HTTP_AUTHORIZATION=token,
            data=self.reply_data2,
        )
        self.assertEqual(response.data['error'], 'Reply with that ID not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)