from django.urls import path
from .views import RetrieveProfileAPIView

urlpatterns = [
    path('profiles/<username>/', RetrieveProfileAPIView.as_view(), name='profile')
]