from typing import List

from debug_toolbar.panels import Panel
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from openfeature.api import add_hooks, get_provider_metadata
from openfeature.flag_evaluation import FlagEvaluationDetails
from openfeature.hook import Hook, HookContext

from django_openfeature import get_evaluation_context


class DebugToolbarHook(Hook):
    def __init__(self):
        self.evaluations = []

    def after(
        self, hook_context: HookContext, details: FlagEvaluationDetails, hints: dict
    ):
        self.evaluations.append(details)

    def extract_evaluations(self) -> List[FlagEvaluationDetails]:
        evaluations = self.evaluations
        self.evaluations = []
        return evaluations


hook = DebugToolbarHook()
add_hooks([hook])


class FeatureFlagsPanel(Panel):
    title = _("Feature Flags")
    template = "debug_toolbar/panels/feature_flags.html"

    @property
    def nav_subtitle(self):
        stats = self.get_stats()
        count = len(stats["flag_evaluations"])
        return ngettext("%d flag evaluation", "%d flag evaluations", count) % count

    def generate_stats(self, request, response):
        evaluation_context = get_evaluation_context(request)
        # TODO: add domain name to the evaluation table
        # TODO: add support for multiple domains
        self.record_stats(
            {
                "flag_evaluations": hook.extract_evaluations(),
                "targeting_key": evaluation_context.targeting_key,
                "attributes": evaluation_context.attributes,
                "providers": {"default": get_provider_metadata()},
            }
        )
