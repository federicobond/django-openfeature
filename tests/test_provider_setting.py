from django.test import TestCase, override_settings
from openfeature import api
from openfeature.provider.no_op_provider import NoOpProvider

from django_openfeature.provider import DjangoTestProvider


class DummyProvider(NoOpProvider):
    pass


def dummy_provider_factory():
    return DummyProvider()


class ProviderSettingTests(TestCase):
    # NOTE: api.get_client().provider is an undocumented property

    def test_provider_set_from_settings_on_app_ready(self):
        self.assertIsInstance(api.get_client().provider, DjangoTestProvider)

    def test_override_settings_swaps_and_restores_provider(self):
        with override_settings(
            OPENFEATURE={"PROVIDER": "tests.test_provider_setting.DummyProvider"}
        ):
            self.assertIsInstance(api.get_client().provider, DummyProvider)
        self.assertIsInstance(api.get_client().provider, DjangoTestProvider)

    def test_provider_factory_function(self):
        with override_settings(
            OPENFEATURE={
                "PROVIDER": "tests.test_provider_setting.dummy_provider_factory"
            }
        ):
            self.assertIsInstance(api.get_client().provider, DummyProvider)

    def test_none_provider_leaves_current_provider_untouched(self):
        with override_settings(OPENFEATURE={}):
            self.assertIsInstance(api.get_client().provider, DjangoTestProvider)
