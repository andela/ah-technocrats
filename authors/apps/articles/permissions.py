from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Class to allow only the author of an article to edit the article.
    """

    def has_object_permission(self, request, view, obj):
        """
        If owner return true, otherwise return false.
        """
        # Non-owner has read permissions only
        # Safe methods include GET, HEAD and OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Give the owner only write permissions
        return obj.author == request.user
