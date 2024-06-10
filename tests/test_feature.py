from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django_openfeature import feature, get_evaluation_context
from django_openfeature.test import override_feature
from openfeature import api as openfeature_api
from openfeature.evaluation_context import EvaluationContext
from openfeature.hook import Hook


class FeatureTests(TestCase):
    def test_feature(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create()
        self.assertFalse(feature(request, "foo", False))

    def test_get_evaluation_context(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create(username="foo", email="foo@example.org")
        self.assertEqual(
            get_evaluation_context(request),
            EvaluationContext(
                str(request.user.pk), {"username": "foo", "email": "foo@example.org"}
            ),
        )

    def test_feature_templetag(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create()
        template = Template("""
            {% load openfeature %}
            {% feature "foo" True as has_foo_enabled %}
            {% if has_foo_enabled %}Foo{% endif %}
        """)
        context = Context({"request": request})
        self.assertIn("Foo", template.render(context))

    @override_feature("foo", True)
    def test_iffeature_templetag(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create()
        template = Template("""
            {% load openfeature %}
            {% iffeature "foo" %}Foo{% endif %}
        """)
        context = Context({"request": request})
        self.assertIn("Foo", template.render(context))

    @override_feature("foo", True)
    def test_iffeature_templetag_evaluates_once(self):
        request = RequestFactory().get("/")

        class CountEvaluationsHook(Hook):
            def __init__(self):
                self.evaluation_count = 0

            def after(self, hook_context, details, hints):
                self.evaluation_count += 1

        hook = CountEvaluationsHook()

        openfeature_api.add_hooks([hook])
        request.user = User.objects.create()
        template = Template("""
            {% load openfeature %}
            {% iffeature "foo" %}Foo1{% endif %}
            {% iffeature "foo" %}Foo2{% endif %}
        """)
        context = Context({"request": request})
        self.assertIn("Foo1", template.render(context))
        self.assertIn("Foo2", template.render(context))
        self.assertEqual(hook.evaluation_count, 2)

        openfeature_api.clear_hooks()
