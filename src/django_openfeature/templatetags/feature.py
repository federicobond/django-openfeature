from django import template

from django_openfeature import feature as _feature

register = template.Library()


@register.simple_tag(takes_context=True)
def feature(context, key: str, default_value: bool):
    return _feature(context["request"], key, default_value)
