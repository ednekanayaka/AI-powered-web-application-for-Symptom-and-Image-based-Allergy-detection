from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        try:
            from django.core.management import call_command
            call_command('seed_data', verbosity=1)
        except Exception as e:
            print(f"[seed_data] Skipped: {e}")
