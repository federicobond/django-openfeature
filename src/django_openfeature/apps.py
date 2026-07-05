from django.apps import AppConfig

from .settings import setup_provider


class DjangoOpenFeatureConfig(AppConfig):
    name = "django_openfeature"
    verbose_name = "Django OpenFeature"

    def ready(self) -> None:
        setup_provider()
