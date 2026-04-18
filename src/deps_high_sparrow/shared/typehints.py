from typing import Any, Optional, TypedDict

__all__ = ["ExtractionField"]


class ExtractionField(TypedDict):
    code: str
    field_type: str
    required: bool
    field_data: Optional[dict[str, Any]]
