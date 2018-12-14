from django.db import models

class Profile(models.Model):
    """
    Profile class.
    """
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
    # Add fields for followers and following
    # Followers are those that follow the user
    # Following are for those that the user follows
    following = models.ManyToManyField("self", related_name="user_following", symmetrical=False)
  
    def __str__(self):
        '''format the returned profile string'''
        return self.user.username

    def follow_author(self, author):
        """
        Method for following an author.
        """
        self.following.add(author)

    def unfollow_author(self, author):
        """
        Method for unfollowing an author.
        """
        self.following.remove(author)

    def retrieve_following(self):
        """
        Get all the authors that the user follows.
        """
        return self.following.all()

    def retrieve_followers(self):
        """
        Get an author's followers.
        """
        return self.user_following.all()
      