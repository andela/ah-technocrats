from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
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