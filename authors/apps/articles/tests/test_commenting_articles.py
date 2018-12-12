import unittest
from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse

class TestComments(BaseTestCase):
    """ Class for testing comments. """

    # test post comment
    def test_comment_creation(self):
        """ Test commenting on an article. """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        response = self.create_comment(token, article_slug)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Comment Added Succesfully')
        comment_body = self.comment_data['comment']['body']
        self.assertEqual(response.data['comment']['body'], comment_body)

    def test_comment_creation_with_invalid_data(self):
        """ Test creating a comment using invalid/missing data. """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        url = reverse(
            "articles:list-create-comment",
            kwargs={
                'article_slug':article_slug,
            }
        )
        response = self.client.post(
            url,
            data=self.invalid_comment_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data['errors'], dict)
        

    def test_commenting_on_non_existing_article(self):
        """ Test commenting on a missing article.  """
        self.user_signup()
        token = 'Token '+ self.user_login()
        url = reverse(
                "articles:list-create-comment",
                kwargs={
                    'article_slug':'non-existing-article'
                }
            )
        response = self.client.post(
            url,
            data=self.invalid_comment_data,
            format='json',
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article with that slug not found')

    def test_commenting_by_a_non_user(self):
        """ Test a non-user cannot comment. """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        url = reverse(
            "articles:list-create-comment",
            kwargs={
                'article_slug':article_slug,
            }
        )
        response = self.client.post( # send request without authentication token
            url,
            data=self.comment_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    # test getting comment
    def test_getting_comment(self):
        """ Test getting article's comment successfully. """
        response, token, url = self.post_comment(self.comment_data) # create one comment
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.get_comments(token, url)
        self.assertContains(response, 'comments')
        self.assertContains(response, 'commentsCount')
        self.assertIsInstance(response.data['comments'], list)
        self.assertEqual(response.data['commentsCount'], 1)

    def test_getting_a_non_existing_article_comments(self):
        """ Test getting a missing comment. """
        self.user_signup()
        token = self.user_login()
        invalid_url = reverse(
            "articles:list-create-comment",
            kwargs={
                'article_slug':'non-existing-slug'
            }
        )
        response = self.get_comments(token, invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article with this slug not found')

    # test updating comment
    def test_updating_a_comment(self):
        """ Test editing an existing comment. """
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED) # confirm comment creation
        url = url+str(response1.data['comment']['id'])+'/'
        response = self.test_client.put(
            url,
            data=self.comment_data2,
            format='json',
            HTTP_AUTHORIZATION=token, 
        )
        self.assertContains(response, 'message')
        self.assertEqual(response.data['message'], 'Comment Updated Successfully')
        self.assertNotEqual(response1.data['comment']['body'], self.comment_data2['comment']['body'])


    def test_updating_with_invalid_data(self):
        """ Test updating comment using invalid data. """
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED) # confirm comment creation
        url = url+str(response1.data['comment']['id'])+'/'
        response = self.test_client.put(
            url,
            data=self.invalid_comment_data,
            format='json',
            HTTP_AUTHORIZATION=token, 
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_missing_comment(self):
        """ Test updating a non-existent comment. """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        non_exisiting_comment = 2333
        url = reverse(
            "articles:update-delete-comment",
            kwargs={
                'article_slug': article_slug,
                'comment_pk': non_exisiting_comment
            }
        )
        response = self.test_client.put(
                url,
                data=self.comment_data2,
                format='json',
                HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Comment with this ID not found')

    def test_non_logged_in_user_cannot_update(self):
        """ Test a user has to login before updating. """
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED) # confirm comment creation
        url = url+str(response1.data['comment']['id'])+'/'
        response = self.test_client.put( # make request without authentication token
            url,
            data=self.comment_data2,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test deleting comment
    def test_deleting_an_existing_comment(self):
        """ Method for testing deleting an existing comment. """
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED) # confirm comment creation
        url = url+str(response1.data['comment']['id'])+'/'
        response = self.test_client.delete(
            url,
            format='json',
            HTTP_AUTHORIZATION=token, 
        )
        self.assertContains(response, 'message')
        self.assertEqual(response.data['message'], 'Comment deleted successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleting_a_non_existing_comment(self):
        """ Method for testing deleting an existing comment. """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        non_exisiting_comment = 2333
        url = reverse(
            "articles:update-delete-comment",
            kwargs={
                'article_slug': article_slug,
                'comment_pk': non_exisiting_comment
            }
        )
        response = self.test_client.delete(
                url,
                format='json',
                HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Comment with that ID not found')
        
    def test_non_logged_in_user_deletting_comment(self):
        """ Test a user has to login before deleting. """
        response1, token, url = self.post_comment(self.comment_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED) # confirm comment creation
        url = url+str(response1.data['comment']['id'])+'/'
        response = self.test_client.delete( # make request without authentication token
            url,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_comment_for_non_existing_article_slug(self):
        """
        test updating comment for a non existing article slug
        """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        self.create_comment(token, article_slug) # create a valid comment_id
        response = self.test_client.put( # update correct comment_id for wrong article slug
            reverse(
                "articles:update-delete-comment",
                kwargs={
                    'article_slug': 'wrong-article-slug',
                    'comment_pk': 1
                }
            ),
            format='json',
            HTTP_AUTHORIZATION=token,
            data=self.comment_data2,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article with this slug not found')

    def test_deleting_comment_for_non_exisiting_article_slug(self):
        """
        test deleting comment for a non existing article slug
        """
        response = self.create_article()
        self.assertEqual(response[1].status_code, status.HTTP_201_CREATED) # confirm artcle creation
        article_slug = response[1].data['slug']
        token = response[2]
        res = self.create_comment(token, article_slug) # create a valid comment_id, id 3
        response = self.test_client.delete( # update correct comment_id for wrong article slug
            reverse(
                "articles:update-delete-comment",
                kwargs={
                    'article_slug': 'wrong-article-slug',
                    'comment_pk': 3
                }
            ),
            format='json',
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Article with that slug not found')