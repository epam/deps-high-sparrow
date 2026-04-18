from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.api.endpoint_marker import MarkerRoute
from deps_high_sparrow.api.endpoint_visibility import Visibility
from deps_high_sparrow.api.serializers.v1 import (
    CreateCrossFieldValidatorRequest,
    CrossFieldValidatorCreatedResponse,
    UpdateCrossFieldValidatorRequest,
    UpdateCrossFieldValidatorResponse,
)
from deps_high_sparrow.application import DocumentTypeService
from deps_high_sparrow.containers import Containers

__all__ = ["cross_field_validator_router"]

cross_field_validator_router = APIRouter(
    prefix="/document-types/{documentTypeId}/cross-field-validators",
    route_class=MarkerRoute,
    tags=["CrossFieldValidator"],
)


@cross_field_validator_router.post(
    "",
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=status.HTTP_201_CREATED,
    response_model=CrossFieldValidatorCreatedResponse,
)
@inject
def add_cross_field_validator(
    validator_data: CreateCrossFieldValidatorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
) -> CrossFieldValidatorCreatedResponse:
    validator_id = application.add_cross_field_validator(
        tenant_id=current_tenant,
        document_type_id=document_type_id,
        name=validator_data.name,
        description=validator_data.description,
        rule=validator_data.rule,
        severity=validator_data.severity,
        validated_fields=validator_data.validated_fields,
        issue_message=validator_data.issue_message,
        dependent_fields=validator_data.dependent_fields,
        for_each=validator_data.for_each,
        for_any=validator_data.for_any,
    )

    return CrossFieldValidatorCreatedResponse(id=validator_id)


@cross_field_validator_router.patch(
    "/{validatorId}",
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=status.HTTP_200_OK,
    response_model=UpdateCrossFieldValidatorResponse,
)
@inject
def update_cross_field_validator(
    validator_data: UpdateCrossFieldValidatorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_id: str = Path(..., alias="validatorId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
) -> UpdateCrossFieldValidatorResponse:
    application.update_cross_field_validator(
        validator_id=validator_id,
        tenant_id=current_tenant,
        document_type_id=document_type_id,
        name=validator_data.name,
        description=validator_data.description,
        rule=validator_data.rule,
        severity=validator_data.severity,
        validated_fields=validator_data.validated_fields,
        issue_message=validator_data.issue_message,
        dependent_fields=validator_data.dependent_fields,
        for_each=validator_data.for_each,
        for_any=validator_data.for_any,
    )

    return UpdateCrossFieldValidatorResponse(id=validator_id)


@cross_field_validator_router.delete(
    "/{validatorId}",
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
def delete_cross_field_validator(
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_id: str = Path(..., alias="validatorId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
):
    application.delete_cross_field_validator(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        validator_id=validator_id,
    )
