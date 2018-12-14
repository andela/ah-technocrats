from django.urls import path
from .views import RetrieveProfileAPIView, FollowProfileAPIView, RetrieveFollowersAPIView, RetrieveFollowingAPIView

urlpatterns = [
    path('profiles/<username>/', RetrieveProfileAPIView.as_view(), name='profile'),
    path('profiles/<username>/follow', FollowProfileAPIView.as_view(), name='follow'),
    path('profiles/<username>/followers', RetrieveFollowersAPIView.as_view(), name='followers'),
    path('profiles/<username>/following', RetrieveFollowingAPIView.as_view(), name='following')
]
