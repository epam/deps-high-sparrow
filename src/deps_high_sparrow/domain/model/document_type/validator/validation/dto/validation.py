from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationResultDTO:
    is_valid: bool = True
    detail: List = field(default_factory=list)
