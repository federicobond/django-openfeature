from collections import ChainMap
from typing import Any, Dict, List, Optional, Union

from openfeature.evaluation_context import EvaluationContext
from openfeature.exception import TypeMismatchError
from openfeature.flag_evaluation import FlagResolutionDetails, Reason
from openfeature.hook import Hook
from openfeature.provider import AbstractProvider, FeatureProvider
from openfeature.provider.metadata import Metadata
from openfeature.provider.no_op_provider import NoOpProvider


class DjangoTestProvider(AbstractProvider):
    _chained: FeatureProvider
    _overrides: ChainMap

    def __init__(self) -> None:
        self._chained = NoOpProvider()
        self._overrides = ChainMap()

    def get_metadata(self) -> Metadata:
        return Metadata(name="Django Test Provider")

    def get_provider_hooks(self) -> List[Hook]:
        return []

    def push_overrides(self, overrides: Dict[str, Any]) -> None:
        self._overrides.maps.insert(0, overrides)

    def pop_overrides(self) -> None:
        self._overrides.maps.pop(0)

    def resolve_boolean_details(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[bool]:
        if flag_key in self._overrides:
            value = self._overrides[flag_key]
            if not isinstance(value, bool):
                raise TypeMismatchError(f"Expected type bool but got {type(value)}")
            return FlagResolutionDetails(
                value=value,
                reason=Reason.STATIC,
                variant="Overridden for test",
            )
        return self._chained.resolve_boolean_details(
            flag_key, default_value, evaluation_context
        )

    def resolve_string_details(
        self,
        flag_key: str,
        default_value: str,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[str]:
        if flag_key in self._overrides:
            value = self._overrides[flag_key]
            if not isinstance(value, str):
                raise TypeMismatchError(f"Expected type str but got {type(value)}")
            return FlagResolutionDetails(
                value=value,
                reason=Reason.STATIC,
                variant="Overridden for test",
            )
        return self._chained.resolve_string_details(
            flag_key, default_value, evaluation_context
        )

    def resolve_integer_details(
        self,
        flag_key: str,
        default_value: int,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[int]:
        if flag_key in self._overrides:
            value = self._overrides[flag_key]
            if not isinstance(value, int):
                raise TypeMismatchError(f"Expected type int but got {type(value)}")
            return FlagResolutionDetails(
                value=value,
                reason=Reason.STATIC,
                variant="Overridden for test",
            )
        return self._chained.resolve_integer_details(
            flag_key, default_value, evaluation_context
        )

    def resolve_float_details(
        self,
        flag_key: str,
        default_value: float,
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[float]:
        if flag_key in self._overrides:
            value = self._overrides[flag_key]
            if not isinstance(value, float):
                raise TypeMismatchError(f"Expected type float but got {type(value)}")
            return FlagResolutionDetails(
                value=value,
                reason=Reason.STATIC,
                variant="Overridden for test",
            )
        return self._chained.resolve_float_details(
            flag_key, default_value, evaluation_context
        )

    def resolve_object_details(
        self,
        flag_key: str,
        default_value: Union[dict, list],
        evaluation_context: Optional[EvaluationContext] = None,
    ) -> FlagResolutionDetails[Union[dict, list]]:
        if flag_key in self._overrides:
            value = self._overrides[flag_key]
            if not isinstance(value, (dict, list)):
                raise TypeMismatchError(
                    f"Expected type dict or list but got {type(value)}"
                )
            return FlagResolutionDetails(
                value=value,
                reason=Reason.STATIC,
                variant="Overridden for test",
            )
        return self._chained.resolve_object_details(
            flag_key, default_value, evaluation_context
        )
