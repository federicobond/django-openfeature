from unittest import TestCase

from django_openfeature.provider import DjangoTestProvider
from django_openfeature.test import override_feature
from openfeature.api import get_client, set_provider
from openfeature.provider.no_op_provider import NoOpProvider


class OverrideFeatureTests(TestCase):
    def test_override_feature_requires_django_test_provider(self):
        set_provider(NoOpProvider())

        @override_feature("foo", True)
        def function():
            pass

        with self.assertRaisesRegex(ValueError, r"requires a DjangoTestProvider"):
            function()

    def test_override_feature(self):
        set_provider(DjangoTestProvider())

        @override_feature("foo", True)
        def function():
            return get_client().get_boolean_value("foo", False)

        self.assertTrue(function())

    def test_override_feature_nested(self):
        set_provider(DjangoTestProvider())

        @override_feature("foo", "foo")
        @override_feature("bar", "bar")
        def function():
            foo = get_client().get_string_value("foo", "")
            bar = get_client().get_string_value("bar", "")
            return foo + bar

        self.assertEqual(function(), "foobar")

    def test_override_feature_as_context_manager(self):
        set_provider(DjangoTestProvider())

        with override_feature("foo", True):
            self.assertTrue(get_client().get_boolean_value("foo", False))
