def test_saving_validation_result_with_issues__ok(
    validation_result_repository,
    validation_result,
):
    validation_result_repository.save(validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            validation_result.id.value, validation_result.tenant_id.value
        )
        == validation_result
    )


def test_saving_empty_validation_result__ok(
    validation_result_repository,
    empty_validation_result,
):
    validation_result_repository.save(empty_validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            empty_validation_result.id.value, empty_validation_result.tenant_id.value
        )
        == empty_validation_result
    )


def test_saving_existing_validation_result__issues_updated(
    validation_result_repository,
    empty_validation_result,
    issues,
):
    validation_result_repository.save(empty_validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            empty_validation_result.id.value, empty_validation_result.tenant_id.value
        )
        == empty_validation_result
    )

    empty_validation_result.add_issues(issues)

    validation_result_repository.save(empty_validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            empty_validation_result.id.value, empty_validation_result.tenant_id.value
        )
        == empty_validation_result
    )


def test_deleting_existing_validation_result__deleted(
    validation_result_repository,
    validation_result,
):
    validation_result_repository.save(validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            validation_result.id.value, validation_result.tenant_id.value
        )
        == validation_result
    )

    validation_result_repository.delete(validation_result.id.value, validation_result.tenant_id.value)

    assert (
        validation_result_repository.validation_result_of_id(
            validation_result.id.value, validation_result.tenant_id.value
        )
        is None
    )


def test_delete_non_existing_validation_result__no_error(
    validation_result_repository,
    validation_result,
):
    validation_result_repository.delete(validation_result.id.value, validation_result.tenant_id.value)


def test_find_non_existing_validation_result__none(
    validation_result_repository,
    validation_result,
):
    assert (
        validation_result_repository.validation_result_of_id(
            validation_result.id.value, validation_result.tenant_id.value
        )
        is None
    )


def test_find_existing_validation_result__ok(
    validation_result_repository,
    validation_result,
):
    validation_result_repository.save(validation_result)

    assert (
        validation_result_repository.validation_result_of_id(
            validation_result.id.value, validation_result.tenant_id.value
        )
        == validation_result
    )
