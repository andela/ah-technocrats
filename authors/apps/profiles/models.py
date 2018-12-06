from django.db import models

class Profile(models.Model):
    bio = models.TextField(blank=True)
    avatar = models.URLField(
        blank=True,
        default='https://libertv.com/wp-content/uploads/2018/03/user-avatar-placeholder-1.png'
     ) 
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''format the returned profile string'''
        return self.user.username
