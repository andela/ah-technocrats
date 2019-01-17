from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """class for serializing the user profile"""
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    last_login = serializers.CharField(source='user.last_login', allow_blank=True)
    country = serializers.CharField(allow_blank=True, required=False)
    website = serializers.URLField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField()
    avatar = serializers.URLField(allow_blank=True, required=False)
    notifications_enabled = serializers.BooleanField()

    phone = serializers.RegexField(
        regex="^[0-9]",
        max_length=12,
        min_length=10,
        error_messages={
            "invalid": "This field should only contain numbers.",
            "max_length": "Phone Number cannot be longer than 10 characters",
            "min_length": "Phone Number cannot be less than 12 characters"
        },
        allow_blank=True
    )

    class Meta:
        model = Profile
        fields = (
            'username',
            'email',
            'last_login',
            'country',
            'website',
            'phone',
            'bio',
            'created_at',
            'avatar',
            'notifications_enabled',
        )
