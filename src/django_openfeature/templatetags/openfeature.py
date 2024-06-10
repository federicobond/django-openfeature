from django.template.base import (
    Node,
    NodeList,
    TemplateSyntaxError,
)
from django.template.library import Library

from django_openfeature import feature as _feature

register = Library()


@register.simple_tag(takes_context=True)
def feature(context, key: str, default_value: bool):
    return _feature(context["request"], key, default_value)


class TemplateFeatureFlagParser:
    def __init__(self, parser, tokens):
        self.template_parser = parser
        self.tokens = tokens

    def parse(self):
        if len(self.tokens) != 1:
            raise TemplateSyntaxError(
                "iffeature tag requires exactly one argument, the flag key"
            )
        value = self.tokens[0]
        return FlagCondition(self.template_parser.compile_filter(value))


class FlagCondition:
    def __init__(self, flag_key):
        self.flag_key = flag_key

    def eval(self, context):
        if self.__class__ not in context.render_context:
            context.render_context[self.__class__] = {}
        evaluation_cache = context.render_context[self.__class__]

        flag_key = self.flag_key.resolve(context)
        flag_value = evaluation_cache.get(flag_key)

        if flag_value is None:
            flag_value = _feature(context["request"], flag_key, False)
            evaluation_cache[flag_key] = flag_value

        return flag_value


@register.tag("iffeature")
def do_iffeature(parser, token):
    # {% if ... %}
    bits = token.split_contents()[1:]
    condition = TemplateFeatureFlagParser(parser, bits).parse()
    nodelist = parser.parse(("else", "endif"))
    conditions_nodelists = [(condition, nodelist)]
    token = parser.next_token()

    # {% else %} (optional)
    if token.contents == "else":
        nodelist = parser.parse(("endif",))
        conditions_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% endif %}
    if token.contents != "endif":
        raise TemplateSyntaxError(
            f'Malformed template tag at line {token.lineno}: "{token.contents}"'
        )

    return IfFeatureNode(conditions_nodelists)


class IfFeatureNode(Node):
    def __init__(self, conditions_nodelists):
        self.conditions_nodelists = conditions_nodelists

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __iter__(self):
        for _, nodelist in self.conditions_nodelists:
            yield from nodelist

    @property
    def nodelist(self):
        return NodeList(self)

    def render(self, context):
        for condition, nodelist in self.conditions_nodelists:
            match = condition.eval(context) if condition else True
            if match:
                return nodelist.render(context)

        return ""
