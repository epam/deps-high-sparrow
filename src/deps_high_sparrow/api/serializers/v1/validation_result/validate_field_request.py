from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["ValidateFieldRequest"]


class ValidateFieldRequest(ConfiguredBaseModel):
    document_id: str = Field(..., alias="documentId")
