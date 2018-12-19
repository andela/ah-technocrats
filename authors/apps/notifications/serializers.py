from rest_framework import serializers
from .models import Notification
from authors.apps.articles.serializers import ArticleSerializer
from django.utils.timesince import timesince


class NotificationSerializer(serializers.ModelSerializer):
    article = ArticleSerializer('article')
    timestance = serializers.SerializerMethodField(method_name='read')

    class Meta:
        model = Notification
        fields = '__all__'

    def calculate_time(self, instance, now=None):
        """
        Method to get the time difference
        """
        return timesince(instance.created_at, now)

    def read(self, instance):
        """
        Methgod to check if the article has been read
        """
        request = self.context.get('request')
        if request.user in instance.read.all():
            return False
        else:
            return True


