from openfeature import api as openfeature

from .settings import get_config

__all__ = ["feature"]

_of_client = openfeature.get_client()


def get_evaluation_context(request):
    config = get_config()
    return config["CONTEXT_EVALUATOR"](request)


def feature(request, key, default_value):
    context = get_evaluation_context(request)
    if isinstance(default_value, bool):
        return _of_client.get_boolean_value(key, default_value, context)
    if isinstance(default_value, str):
        return _of_client.get_string_value(key, default_value, context)
    if isinstance(default_value, int):
        return _of_client.get_integer_value(key, default_value, context)
    if isinstance(default_value, float):
        return _of_client.get_float_value(key, default_value, context)
    if isinstance(default_value, dict | list):
        return _of_client.get_object_value(key, default_value, context)
    raise ValueError(f"Unsupported default value type: {type(default_value)}")
