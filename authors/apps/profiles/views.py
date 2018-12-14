from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import Profile
from .serializers import ProfileSerializer
from .exceptions import ProfileNotFound

class RetrieveProfileAPIView(RetrieveAPIView):
    """retrieve users profile"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        """retrieve existing user profiles"""
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileNotFound
        serializer = self.serializer_class(profile)
        return Response({
            'profile': serializer.data
        }, status = status.HTTP_200_OK)


class FollowProfileAPIView(CreateAPIView):
    """
    Class for handling following and unfollowing of authors.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request, username):
        """
        Method for following an author.
        """
        user_to_follow = request.data.get('user')
        current_user = request.user.profile

        try:
            # Check if profile to follow exists
            user = Profile.objects.get(
                    user__username=user_to_follow
                )
            # Ensure current user does not follow self
            if current_user == user:
                return Response({'message': "You cannot follow yourself."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                current_user.follow_author(user)
                return Response({'message':"You have successfully followed '{}' ".format(user)}, 
                        status = status.HTTP_200_OK)                 
        except Profile.DoesNotExist:
            raise ProfileNotFound
        
    def delete(self,request, username):
        """
        Method for unfollowing an author.
        """
        user_to_unfollow = request.data.get('user')
        current_user = request.user.profile
        
        try:
            user = Profile.objects.get(
                    user__username=user_to_unfollow
                )
            current_user.unfollow_author(user)
            return Response({'message':"You have successfully unfollowed '{}' ".format(user)},
                    status = status.HTTP_200_OK)
        except Profile.DoesNotExist:
            raise ProfileNotFound


class RetrieveFollowingAPIView(RetrieveAPIView):
    """
    Class for handling authors that the user follows.
    """
    permission_class = (IsAuthenticated,)
    serializer_class = ProfileSerializer

        
    def get(self, request, username):
        """
        Retrieve all the users that a user follows.
        """
        user_profile = request.user.profile
        following = user_profile.retrieve_following()
        
        serializer = ProfileSerializer(following, many=True)
        message = {'message':"Authors that you follow.",
                    'following': serializer.data}        
        return Response(message, status=status.HTTP_200_OK)


class RetrieveFollowersAPIView(RetrieveAPIView):
    """
    Class to handle getting followers.,                                                   
    """
    permission_class = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, username):
        """
        Get an author's followers.
        """
        user_profile = request.user.profile
        user = Profile.objects.get(user__username=username)
        followers = user_profile.retrieve_followers()
        serializer = self.serializer_class(followers, many=True)
        message = {'message':"followers found.",
                    'followers': serializer.data}
        return Response(message, status=status.HTTP_200_OK)
