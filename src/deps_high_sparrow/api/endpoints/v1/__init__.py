from fastapi import APIRouter

from deps_high_sparrow.constants import V1_PREFIX

from .cross_field_validator import cross_field_validator_router
from .document_type import document_type_router
from .rule import rule_router
from .validation_result import validation_result_router

__all__ = ["v1_router"]

v1_router = APIRouter(prefix=V1_PREFIX)
v1_router.include_router(rule_router)
v1_router.include_router(document_type_router)
v1_router.include_router(validation_result_router)
v1_router.include_router(cross_field_validator_router)
