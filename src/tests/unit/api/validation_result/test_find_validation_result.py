from http import HTTPStatus

import pytest

from deps_high_sparrow.constants import V1_API_PREFIX
from deps_high_sparrow.domain.model import IValidationResultRepository


@pytest.mark.validation_result
def test_find__validation_result_exists__ok(
    client,
    validation_result_with_issues,
    fake_validation_result_repository: IValidationResultRepository,
):
    fake_validation_result_repository.save(validation_result_with_issues)

    response = client.get(f"{V1_API_PREFIX}/results/{validation_result_with_issues.id()}")
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_dict["isValid"] == validation_result_with_issues.is_valid
    assert len(response_dict["detail"]) == len(validation_result_with_issues.issues) == 1
    assert response_dict["detail"][0]["fieldCode"] == list(validation_result_with_issues.issues.keys())[0]


@pytest.mark.validation_result
def test_find__validation_result_exists__not_found(
    client,
    validation_result_with_issues,
):
    response = client.get(f"{V1_API_PREFIX}/results/{validation_result_with_issues.id()}")

    assert response.status_code == HTTPStatus.NOT_FOUND
