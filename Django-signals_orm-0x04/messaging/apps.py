from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        # Ensures our signal handlers get registered
        import messaging.signals  # noqa
