from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.api.endpoint_marker import MarkerRoute
from deps_high_sparrow.api.endpoint_visibility import Visibility
from deps_high_sparrow.api.serializers.v1 import SerializedValidationResult
from deps_high_sparrow.application import ValidationResultService
from deps_high_sparrow.containers import Containers

__all__ = ["validation_result_router"]

validation_result_router = APIRouter(prefix="/results", route_class=MarkerRoute, tags=["Validation Result"])


@validation_result_router.get(
    "/{entityId}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedValidationResult,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def find_validation_result(
    entity_id: str = Path(..., alias="entityId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: ValidationResultService = Depends(Provide[Containers.application.validation_result]),
) -> SerializedValidationResult:
    validation_result = application.find_validation_result(
        entity_id=entity_id,
        tenant_id=current_tenant,
    )

    return SerializedValidationResult.from_model(validation_result)
