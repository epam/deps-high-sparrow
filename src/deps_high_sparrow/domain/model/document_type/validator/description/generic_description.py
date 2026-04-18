import abc

from .description import Description

__all__ = ["GenericDescription"]


class GenericDescription(Description, abc.ABC):
    ...  # noqa: WPS604
