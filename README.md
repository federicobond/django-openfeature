django-openfeature
==================

![build status](https://github.com/federicobond/django-openfeature/actions/workflows/python-package.yml/badge.svg?branch=main)
![release](https://img.shields.io/pypi/v/django-openfeature)
![python versions](https://img.shields.io/pypi/pyversions/django-openfeature)

> ⚠️ Caution: this repository is a work-in-progress. ⚠️

Django OpenFeature is a set of utilities to use OpenFeature in your Django applications.

## Features

 * Django Debug Toolbar integration
 * Templatetags for flag evaluation
 * Automatic evaluation context from request
 * Flag override mechanism for testing

## Installation

```
pip install django-openfeature
```

Add `django_openfeature` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    # ...
    'django_openfeature',
    # ...
]
```

## Usage

### Flag Evaluation Helpers

django-openfeature provides a set of helpers to evaluate a feature flag:

```python
from django_openfeature import feature

feature(request, 'my_feature', False)
```

The `feature` function will infer the type of the feature flag based on the default value provided
and call the appropriate resolver method.

It will also create an evaluation context from the request. This context can be configured via the
`OPENFEATURE` setting (described below).

Inside templates, you can use the `feature` template tag to evaluate feature flags. Remember to load the
`openfeature` library first.

```html
{% load openfeature %}

{% feature 'my_feature' False as my_feature_enabled %}
{% if my_feature_enabed %}
    <p>Feature is enabled</p>
{% else %}
    <p>Feature is disabled</p>
{% endif %}
```

As an alternative to evaluating feature flags to a variable you can use the `iffeature` template tag.
It will output the contents of the block if the boolean flag resolves to True. It supports a single
`{% else %}` clause that will be displayed otherwise.

```html
{% load openfeature %}

{% iffeature 'my_feature' %}
    <p>Feature is enabled</p>
{% else %}
    <p>Feature is disabled</p>
{% endif %}
```

### Configuration

```python
OPENFEATURE = {
    "CONTEXT_EVALUATOR": "myapp.utils.get_evaluation_context",
}
```

The `CONTEXT_EVALUATOR` setting should point to a function that receives a request and returns an OpenFeature EvaluationContext as defined in the `openfeature-sdk` package.

Alternatively, the context evaluator can point to a class that produces callable instances with the same signature. The default context evaluator is `django_openfeature.context.OpenFeatureContext` and looks roughly like this:

```python
class OpenFeatureContext:
    targeting_key = "id"
    targeting_key_anonymous = "unknown"
    user_attributes = ("username", "email")

    def get_context(self, request):
        user = request.user
        if not user or user.is_anonymous:
            return EvaluationContext(self.targeting_key_anonymous)
        return self.get_user_context(user)

    def get_user_context(self, user):
        attributes = {}
        for attr in self.user_attributes:
            attributes[attr] = getattr(user, attr)
        targeting_key = str(getattr(user, self.targeting_key))
        return EvaluationContext(targeting_key, attributes)

    def __call__(self, request):
        return self.get_context(request)
```

Use this class as base to declaratively define your own context evaluator. For example, to change the targeting key to the
user's username:

```python
from django_openfeature.context import OpenFeatureContext

class MyOpenFeatureContext(OpenFeatureContext):
    targeting_key = "username"
```

Then in your settings:

```python
OPENFEATURE = {
    "CONTEXT_EVALUATOR": "myapp.utils.MyOpenFeatureContext",
}
```

### Debug Toolbar Panel

django-openfeature comes with a Feature Flags panel for the Django Debug Toolbar. You can activate it by adding `openfeature.debug_toolbar.panels.FeatureFlagsPanel` to your `DEBUG_TOOLBAR_PANELS` setting.

```python
DEBUG_TOOLBAR_PANELS = [
    # ...
    'openfeature.debug_toolbar.panels.FeatureFlagsPanel',
    # ...
]
```

The Feature Flags panel will show you the feature flag evaluations for the current request, the request evaluation context
and the configured providers for those evaluations.

<img width="928" alt="Feature Flags Debug Toolbar Panel" src="https://github.com/federicobond/django-openfeature/assets/138426/b22d5e1c-ac93-4a1f-af8d-e0206abc6c02">


### Testing Utilities

django-openfeature provides a set of utilities to help you test your feature flags. To use them, you must set the provider to an instance of `django_openfeature.provider.DjangoTestProvider` in your test settings.

```python
# in your test settings
import openfeature.api
from django_openfeature.provider import DjangoTestProvider

openfeature.api.set_provider(DjangoTestProvider())
```

`override_feature` is a function decorator that allows you to override the value of a feature flag for the duration of a test.

```python
from django_openfeature.test import override_feature

@override_feature('my_feature', True)
def test_my_feature_enabled(self):
    # ...
```

Decorators can be stacked to override multiple feature flags.

You can also use `override_feature` as a context manager.

```python
from django_openfeature.test import override_feature

def test_my_feature_enabled(self):
    with override_feature('my_feature', True):
        # ...
```

## TODO

 * [ ] Add support for OpenFeature domains (requires SDK release)

## License

MIT License
