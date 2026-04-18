import copy

import pytest
from pydantic import ValidationError

from deps_high_sparrow.api.serializers.v1 import UpdateCrossFieldValidatorRequest


class TestUpdateCrossFieldValidatorRequest:
    def test_valid_update_request(self, crossfield_validator_data):
        request = UpdateCrossFieldValidatorRequest(**crossfield_validator_data)
        assert request.name == crossfield_validator_data["name"]
        assert request.rule == crossfield_validator_data["rule"]
        assert request.for_each == crossfield_validator_data["for_each"]
        assert request.for_any == crossfield_validator_data["for_any"]

    def test_partial_update_request(self):
        partial_data = {"name": "partial_update", "description": "partial update description"}
        request = UpdateCrossFieldValidatorRequest(**partial_data)
        assert request.name == "partial_update"
        assert request.description == "partial update description"
        assert request.rule is None
        assert request.validated_fields is None

    @pytest.mark.parametrize(
        "field_name, invalid_value",
        [
            ("validated_fields", []),
        ],
    )
    def test_update_request_with_empty_fields(self, crossfield_validator_data, field_name, invalid_value):
        data = copy.deepcopy(crossfield_validator_data)
        data[field_name] = invalid_value

        with pytest.raises(ValidationError) as exc_info:
            UpdateCrossFieldValidatorRequest(**data)

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
    def test_update_request_with_invalid_strings(self, crossfield_validator_data, field_name, invalid_value):
        data = copy.deepcopy(crossfield_validator_data)
        data[field_name] = invalid_value

        with pytest.raises(ValidationError) as exc_info:
            UpdateCrossFieldValidatorRequest(**data)

        error_msg = str(exc_info.value)
        assert "cannot be empty or contain only whitespace or special characters." in error_msg

    def test_update_request_with_for_each_for_any(self, crossfield_validator_data):
        data = copy.deepcopy(crossfield_validator_data)

        data["for_each"] = True
        data["for_any"] = True
        request = UpdateCrossFieldValidatorRequest(**data)
        assert request.for_each is True
        assert request.for_any is True
