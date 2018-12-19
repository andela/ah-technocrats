#tests/test_notifications.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from .models import Notification
from authors.apps.profiles.models import Profile


class NotificationView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        """
        Mark a notification as read
        """
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                "error": "Notification does not exist"
            }, status.HTTP_404_NOT_FOUND)
        user = request.user
        if user in notification.notified.all() or user in notification.notify_comments.all():
            notification.read.add(user.id)
            response = {"message": "The notification has been marked as read"}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Sorry, this notification is not yours"
            }, status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        """
        Delete a given notification using it's id.
        """
        try:
            my_notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                "error": "Notification not found"
            }, status.HTTP_404_NOT_FOUND)
        # check if the notification exists
        user = request.user
        if user in my_notification.notified.all() or user in my_notification.notify_comments.all():
            my_notification.notified.remove(user.id)
            response = {"message": "Notification has been successfully deleted."}
            return Response(response, status=status.HTTP_200_OK)
        else:
            # prevent a user from deleting an notification they do not own
            return Response({
                "error": "You cannot perform this action. Ensure this notification belongs to you"
            }, status.HTTP_403_FORBIDDEN)


class NotificationAPIView(APIView):
    """
    Class to get all notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Method to retrieve all notifications from the database for a user
        """
        user = request.user
        notifications = Notification.objects.all()
        data = {}
        for notification in notifications:
            if user in notification.notified.all() or user in notification.notify_comments.all():
                serializer = self.serializer_class(
                    notification, context={'request': request})
                data[notification.id] = serializer.data
            
        return Response(data, status=status.HTTP_200_OK)
