"""register the signal handler for creating the new 
    user profile upon successful registration"""

from django.apps import AppConfig

class AuthAppConfig(AppConfig):
    """define the app config"""

    label = 'authentication'
    name = 'authors.apps.authentication'
    verbose_name = 'Authentication'

    def ready(self):
        """register the signal handler when the app is ready"""

        import authors.apps.authentication.signals

default_app_config = 'authors.apps.authentication.AuthAppConfig'