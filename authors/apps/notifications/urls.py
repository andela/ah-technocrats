
from django.urls import path
from .views import NotificationView, NotificationAPIView
# app_name = 'notifications'
urlpatterns = [
    path('notifications/<str:pk>', NotificationView.as_view(), name='one_notification'),
    path('notifications/', NotificationAPIView.as_view(), name='all_notifications'),

]
