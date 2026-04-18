from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_high_sparrow.api.auth import get_current_user_tenant
from deps_high_sparrow.api.endpoint_marker import MarkerRoute
from deps_high_sparrow.api.endpoint_visibility import Visibility
from deps_high_sparrow.api.serializers.v1 import CreateRuleRequest, SerializedRule
from deps_high_sparrow.application import RuleService
from deps_high_sparrow.constants import ENCODED_SLASH
from deps_high_sparrow.containers import Containers

__all__ = ["rule_router"]

rule_router = APIRouter(
    prefix="/document-types/{documentTypeId}/validators/{validatorCode}",
    route_class=MarkerRoute,
    tags=["Rule"],
)


@rule_router.post(
    "/rules",
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedRule,
)
@inject
def create_rule(
    rule_data: CreateRuleRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: RuleService = Depends(Provide[Containers.application.rule]),
) -> SerializedRule:
    rule = application.create_rule(
        tenant_id=current_tenant,
        document_type_id=document_type_id,
        validator_code=validator_code,
        name=rule_data.name,
        severity=rule_data.severity,
        rule=rule_data.rule,
        issue_message=rule_data.issue_message,
        description=rule_data.description,
        need_warning_even_if_optional=rule_data.need_warning_even_if_optional,
        for_each=rule_data.for_each,
        for_any=rule_data.for_any,
        check_optional_fields=rule_data.check_optional_fields,
    )
    return SerializedRule.from_model(rule)


@rule_router.delete(
    "/rules/{ruleName}",
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=status.HTTP_204_NO_CONTENT,
    description=f"Use `{ENCODED_SLASH}` instead of `/` in the `ruleName` parameter.",
    response_class=Response,
)
@inject
def delete_rule(
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    rule_name: str = Path(..., alias="ruleName"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: RuleService = Depends(Provide[Containers.application.rule]),
):
    application.delete_rule(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        validator_code=validator_code,
        name=rule_name,
    )
