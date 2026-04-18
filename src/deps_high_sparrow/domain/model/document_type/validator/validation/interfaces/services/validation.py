from abc import ABCMeta, abstractmethod
from typing import List, Optional

from ...dto.prepared_field import BaseDataToValidate
from ...dto.validation import ValidationResultDTO
from ...entities import RuleEntity


class IValidationService(metaclass=ABCMeta):
    @abstractmethod
    def validate(
        self,
        fields: List[BaseDataToValidate],
        rules: list[RuleEntity],
        context_fields: Optional[List[BaseDataToValidate]] = None,
    ) -> ValidationResultDTO:
        pass
