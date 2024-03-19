import inspect
from functools import lru_cache

from django.conf import settings
from django.dispatch import receiver
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

CONFIG_DEFAULTS = {
    "CONTEXT_EVALUATOR": "django_openfeature.context.OpenFeatureContext",
}

IMPORT_STRINGS = ["CONTEXT_EVALUATOR"]


@lru_cache(maxsize=None)
def get_config():
    user_config = getattr(settings, "OPENFEATURE", {})
    config = CONFIG_DEFAULTS.copy()
    config.update(user_config)

    for key in IMPORT_STRINGS:
        config[key] = import_string(config[key])
        # instantiate classes
        if inspect.isclass(config[key]):
            config[key] = config[key]()

    return config


@receiver(setting_changed)
def update_openfeature_config(*, setting, **kwargs):
    if setting == "OPENFEATURE":
        get_config.cache_clear()
