# from django.apps import AppConfig


# class AppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'App'
    
    
# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    def ready(self):
        import App.signals  # Import your signals file
