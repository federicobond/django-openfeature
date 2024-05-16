from openfeature.evaluation_context import EvaluationContext


class OpenFeatureContext:
    targeting_key = "id"
    targeting_key_anonymous = "unknown"
    user_attributes = ("username", "email")

    def get_context(self, request) -> EvaluationContext:
        user = request.user
        if not user or user.is_anonymous:
            return EvaluationContext(self.targeting_key_anonymous)
        return self.get_user_context(user)

    def get_user_context(self, user) -> EvaluationContext:
        attributes = {}
        for attr in self.user_attributes:
            if not hasattr(user, attr):
                raise ValueError(f"User model does not have attribute: {attr}")
            attributes[attr] = getattr(user, attr)
        targeting_key = str(getattr(user, self.targeting_key))
        return EvaluationContext(targeting_key, attributes)

    def __call__(self, request) -> EvaluationContext:
        return self.get_context(request)
