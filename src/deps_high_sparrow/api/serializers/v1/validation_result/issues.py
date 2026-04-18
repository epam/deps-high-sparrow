from typing import Optional

from pydantic import Field

from deps_high_sparrow.domain.model import CrossFieldIssues, Issues

from ...base import ConfiguredBaseModel
from .cross_field_issue import SerializedCrossFieldIssue
from .issue import SerializedIssue

__all__ = ["SerializedIssues"]


class SerializedIssues(ConfiguredBaseModel):
    field_code: str = Field(..., alias="fieldCode")
    document_id: str = Field(..., alias="documentId")
    errors: Optional[list[SerializedIssue]]
    warnings: Optional[list[SerializedIssue]]
    cross_field_errors: Optional[list[SerializedCrossFieldIssue]] = Field(alias="crossFieldErrors")
    cross_field_warnings: Optional[list[SerializedCrossFieldIssue]] = Field(alias="crossFieldWarnings")

    @classmethod
    def from_model(
        cls, entity_id: str, issues: Issues, cross_field_issues: dict[str, CrossFieldIssues]
    ) -> "SerializedIssues":
        cross_field_issues_by_code = cross_field_issues.get(issues.code.value)

        return cls(
            field_code=issues.code.value,
            document_id=entity_id,
            errors=[SerializedIssue.from_model(error) for error in issues.errors],
            warnings=[SerializedIssue.from_model(warning) for warning in issues.warnings],
            cross_field_errors=[
                SerializedCrossFieldIssue.from_model(cross_field_issue)
                for cross_field_issue in cross_field_issues_by_code.errors
            ]
            if cross_field_issues_by_code
            else [],
            cross_field_warnings=[
                SerializedCrossFieldIssue.from_model(cross_field_issue)
                for cross_field_issue in cross_field_issues_by_code.warnings
            ]
            if cross_field_issues_by_code
            else [],
        )
