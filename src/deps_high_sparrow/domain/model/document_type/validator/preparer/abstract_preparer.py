import abc

from ....shared import EntityCode
from ...document_artifact import Value
from ..validation.dto.prepared_field import BaseDataToValidate
from ..validator_type import ValidatorType

__all__ = ["AbstractPreparer"]


class AbstractPreparer(abc.ABC):
    def __init__(self, code: EntityCode, type_: ValidatorType, is_required: bool):
        self.code = code
        self.type = type_
        self.is_required = is_required

    @abc.abstractmethod
    def prepare(self, value: Value) -> BaseDataToValidate:
        ...
