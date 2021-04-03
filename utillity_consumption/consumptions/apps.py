from django.apps import AppConfig


class ConsumptionsConfig(AppConfig):
    name = 'utillity_consumption.consumptions'

    def ready(self):
        try:
            import utillity_consumption.users.signals  # noqa F401
        except ImportError:
            pass
