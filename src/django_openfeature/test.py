from contextlib import contextmanager
from typing import Dict, List, Union

from openfeature import api

from django_openfeature.provider import DjangoTestProvider

__all__ = ["override_feature"]


@contextmanager
def override_feature(name: str, value: Union[bool, str, int, float, Dict, List]):
    # NOTE: using undocumented client property to access the provider
    provider = api.get_client().provider
    if not isinstance(provider, DjangoTestProvider):
        raise ValueError(
            "The override_feature decorator requires a DjangoTestProvider to be set."
        )
    provider.push_overrides({name: value})
    try:
        yield
    finally:
        provider.pop_overrides()
