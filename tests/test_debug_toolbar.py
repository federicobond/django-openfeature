from unittest.mock import Mock

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django_openfeature.debug_toolbar.panels import FeatureFlagsPanel
from openfeature.api import get_client
from openfeature.flag_evaluation import FlagEvaluationDetails, Reason
from openfeature.provider import Metadata


class FeatureFlagsPanelTests(TestCase):
    def test_panel(self):
        toolbar = Mock()
        get_response = Mock()
        panel = FeatureFlagsPanel(toolbar, get_response)
        request = RequestFactory().get("/")
        request.user = User.objects.create(
            username="foo",
            email="foo@example.org",
        )
        response = HttpResponse()

        get_client().get_boolean_value("foo", False)

        panel.record_stats = Mock()
        panel.generate_stats(request, response)

        panel.record_stats.assert_called_once_with(
            {
                "flag_evaluations": [
                    FlagEvaluationDetails(
                        flag_key="foo",
                        value=False,
                        variant="Passed in default",
                        flag_metadata={},
                        reason=Reason.DEFAULT,
                    )
                ],
                "targeting_key": "1",
                "attributes": {"username": "foo", "email": "foo@example.org"},
                "providers": {"default": Metadata(name="Django Test Provider")},
            }
        )
