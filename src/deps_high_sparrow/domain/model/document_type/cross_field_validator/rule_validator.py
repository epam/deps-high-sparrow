import ast
import re

from deps_high_sparrow.domain.exceptions import RuleFieldReferencesMismatchError

__all__ = ["RuleFieldReferencesValidator"]

_ITEM_OF_PREFIX = "item_of__"
_COLUMN_SUFFIX_RE = re.compile(r"__\d+$")
_OLD_STYLE_RE = re.compile(r"^type_\w+?__(.+)$")


class RuleFieldReferencesValidator:
    def validate(self, rule: str, validated_fields: list[str], dependent_fields: list[str]) -> None:
        referenced = self._extract_field_codes(rule)
        declared = set(validated_fields + dependent_fields)
        unknown = sorted(referenced - declared)
        unreferenced = sorted(declared - referenced)

        if unknown or unreferenced:
            raise RuleFieldReferencesMismatchError(
                unreferenced_fields=unreferenced,
                unknown_fields=unknown,
            )

    def _extract_field_codes(self, rule: str) -> set[str]:
        field_codes = set()
        for node in ast.walk(ast.parse(rule)):
            if isinstance(node, ast.Name):
                code = self._extract_field_code(node.id)
                if code is not None:
                    field_codes.add(code)

        return field_codes

    def _extract_field_code(self, identifier: str) -> str | None:
        if identifier.startswith("F"):
            return self._strip_item_of_and_column(identifier[1:])
        match = _OLD_STYLE_RE.match(identifier)
        if match:
            return self._strip_item_of_and_column(match.group(1))

        return None

    @staticmethod
    def _strip_item_of_and_column(field_part: str) -> str:
        if field_part.startswith(_ITEM_OF_PREFIX):
            field_part = field_part[len(_ITEM_OF_PREFIX) :]

        return _COLUMN_SUFFIX_RE.sub("", field_part)
