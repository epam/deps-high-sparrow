from typing import Annotated

from pydantic import AfterValidator, AnyHttpUrl

from deps_high_sparrow.domain.model import ExternalValidator

from ..base import ConfiguredBaseModel

__all__ = ["SerializedExternalValidator"]


class SerializedExternalValidator(ConfiguredBaseModel):
    name: str
    url: Annotated[AnyHttpUrl, AfterValidator(str)]

    @classmethod
    def from_model(cls, external_validator: ExternalValidator) -> "SerializedExternalValidator":
        return cls(
            name=external_validator.name,
            url=external_validator.url,
        )
