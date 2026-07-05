import inspect
from functools import lru_cache

from django.conf import settings
from django.dispatch import receiver
from django.test.signals import setting_changed
from django.utils.module_loading import import_string
from openfeature import api

CONFIG_DEFAULTS = {
    "CONTEXT_EVALUATOR": "django_openfeature.context.OpenFeatureContext",
    "PROVIDER": None,
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


def setup_provider():
    """Set the global OpenFeature provider from the PROVIDER setting, if given.

    PROVIDER may be the import path of a provider class, a zero-argument
    factory function, or a provider instance. When it is None (the default),
    the provider is left untouched so it can be configured elsewhere.
    """
    provider = get_config()["PROVIDER"]
    if provider is None:
        return
    if isinstance(provider, str):
        provider = import_string(provider)
    if callable(provider):
        provider = provider()
    api.set_provider(provider)


@receiver(setting_changed)
def update_openfeature_config(*, setting, **kwargs):
    if setting == "OPENFEATURE":
        get_config.cache_clear()
        setup_provider()
