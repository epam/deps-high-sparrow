import pytest
from pydantic import ValidationError

from deps_high_sparrow.api.serializers.v1 import CreateCrossFieldValidatorRequest
from deps_high_sparrow.domain import Severity
from deps_high_sparrow.domain.exceptions import CrossFieldValidatorAlreadyExistsError


class TestCreateCrossFieldValidatorRequest:
    def test_add_cross_field_validator_with_duplicate_name(self, document_type_with_all_validators):
        document_type, _ = document_type_with_all_validators

        with pytest.raises(CrossFieldValidatorAlreadyExistsError):
            document_type.add_cross_field_validator(
                name="test_validator",
                description="Another description",
                rule="field3 == field4",
                severity=Severity.WARNING,
                validated_fields=["field3", "field4"],
                issue_message="Fields ${field3} and ${field4} should match",
                dependent_fields=["field3", "field4"],
            )

    @pytest.mark.parametrize(
        "field_name, invalid_value",
        [
            ("validated_fields", []),
        ],
    )
    def test_create_request_with_empty_fields(self, crossfield_validator_data, field_name, invalid_value):
        crossfield_validator_data[field_name] = invalid_value

        with pytest.raises(ValidationError) as exc_info:
            CreateCrossFieldValidatorRequest(**crossfield_validator_data)

        error_msg = str(exc_info.value)
        assert "Validated fields list cannot be empty. Please provide at least one field." in error_msg

    @pytest.mark.parametrize(
        "field_name, invalid_value",
        [
            ("rule", ""),
            ("rule", " "),
            ("rule", "\n"),
            ("rule", "\t"),
            ("rule", " \n\t "),
            ("issue_message", ""),
            ("issue_message", " "),
            ("issue_message", "\n"),
            ("issue_message", "\t"),
            ("issue_message", " \n\t "),
        ],
    )
    def test_create_request_with_invalid_strings(self, crossfield_validator_data, field_name, invalid_value):
        crossfield_validator_data[field_name] = invalid_value

        with pytest.raises(ValidationError) as exc_info:
            CreateCrossFieldValidatorRequest(**crossfield_validator_data)

        error_msg = str(exc_info.value)
        assert "cannot be empty or contain only whitespace or special characters." in error_msg

    def test_create_request_with_default_dependent_fields(self, crossfield_validator_data):
        crossfield_validator_data.pop("dependent_fields")
        request = CreateCrossFieldValidatorRequest(**crossfield_validator_data)
        assert request.dependent_fields == []

        crossfield_validator_data["dependent_fields"] = None
        request = CreateCrossFieldValidatorRequest(**crossfield_validator_data)
        assert request.dependent_fields == []

        crossfield_validator_data["dependent_fields"] = []
        request = CreateCrossFieldValidatorRequest(**crossfield_validator_data)
        assert request.dependent_fields == []
