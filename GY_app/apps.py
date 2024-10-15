from django.apps import AppConfig


class GyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GY_app'
    
    def ready(self):
        import GY_app.signals
