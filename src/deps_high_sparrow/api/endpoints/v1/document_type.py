from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.api.endpoint_marker import MarkerRoute
from deps_high_sparrow.api.endpoint_visibility import Visibility
from deps_high_sparrow.api.serializers.v1 import (
    AllValidatorsResponse,
    SerializedDocumentType,
    SerializedExternalValidator,
    SerializedValidationResult,
    ValidateFieldRequest,
)
from deps_high_sparrow.application import DocumentTypeService, ValidationResultService
from deps_high_sparrow.containers import Containers

__all__ = ["document_type_router"]

document_type_router = APIRouter(prefix="/document-types", route_class=MarkerRoute, tags=["DocumentType"])


@document_type_router.get(
    "/{documentTypeId}",
    status_code=status.HTTP_200_OK,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def find_document_type(
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
) -> SerializedDocumentType:
    document_type = application.find_document_type(
        tenant_id=current_tenant,
        document_type_id=document_type_id,
    )
    return SerializedDocumentType.from_model(document_type)


@document_type_router.post(
    "/{document_type_id}/external-validators",
    status_code=status.HTTP_201_CREATED,
    openapi_extra={"visibility": Visibility.PUBLIC},
    response_class=Response,
)
@inject
def attach_validator(
    external_validator_data: SerializedExternalValidator,
    document_type_id: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
) -> None:
    application.attach_validator(
        tenant_id=current_tenant,
        document_type_id=document_type_id,
        name=external_validator_data.name,
        url=external_validator_data.url,
    )


@document_type_router.delete(
    "/{document_type_id}/external-validators/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra={"visibility": Visibility.PUBLIC},
    response_class=Response,
)
@inject
def remove_validator(
    document_type_id: str,
    name: str,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
) -> None:
    application.remove_validator(tenant_id=current_tenant, document_type_id=document_type_id, name=name)


@document_type_router.get(
    "/{documentTypeId}/validators",
    status_code=status.HTTP_200_OK,
    openapi_extra={"visibility": Visibility.PUBLIC},
    response_model=AllValidatorsResponse,
)
@inject
def get_validators(
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.application.document_type]),
):
    return AllValidatorsResponse.from_model(
        application.find_document_type(tenant_id=current_tenant, document_type_id=document_type_id),
    )


@document_type_router.post(
    "/{documentTypeId}/validators/{validatorCode}/validate",
    status_code=status.HTTP_200_OK,
    response_model=SerializedValidationResult,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def validate_field(
    request_data: ValidateFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: ValidationResultService = Depends(Provide[Containers.application.validation_result]),
) -> SerializedValidationResult:
    validation_result = application.validate_field(
        document_id=request_data.document_id,
        document_type_id=document_type_id,
        field_code=validator_code,
        tenant_id=current_tenant,
    )

    return SerializedValidationResult.from_model(validation_result)
