from rest_framework.exceptions import APIException

class ProfileNotFound(APIException):
    """define cxustom exeption for non-existing profile"""
    status_code = 404
    default_detail = 'Profile Not Found'
    