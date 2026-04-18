from .base import NotFoundError

__all__ = ["ValidationResultNotFound"]


class ValidationResultNotFound(NotFoundError):
    code = "validation_result_not_found"

    def __init__(self, id_: str) -> None:
        super().__init__(f"Validation result with id: `{id_}` not found")
