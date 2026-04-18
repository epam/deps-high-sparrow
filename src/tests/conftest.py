from uuid import uuid4

import pytest
from fastapi import FastAPI
from pytest_factoryboy import register
from starlette.testclient import TestClient

from deps_high_sparrow.domain import ValidationResult
from deps_high_sparrow.entrypoint import create_fastapi
from tests.factories import (
    DocumentTypeFactory,
    ExternalValidatorFactory,
    IssueFactory,
    IssuesFactory,
    RuleFactory,
    ValidationResultFactory,
)
from tests.factories.cross_field_issue_message import CrossFieldIssueMessageFactory
from tests.factories.cross_field_validator import CrossFieldValidatorFactory
from tests.fakes import FakeCommandProducer, FakeDomainEventPublisher


@pytest.fixture(scope="session")
def app() -> FastAPI:
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def session_containers(app):
    return app.containers


@pytest.fixture
def containers(session_containers):
    with session_containers.reset_singletons() as containers:
        yield containers


@pytest.fixture
def config(containers):
    return containers.config


@pytest.fixture
def repositories(containers):
    return containers.repositories


@pytest.fixture
def external_services(containers):
    return containers.external_services


@pytest.fixture
def application(containers):
    return containers.application


@pytest.fixture
def test_command_channel():
    return None


@pytest.fixture(autouse=True)
def command_producer(containers):
    with containers.command_producer.override(FakeCommandProducer()) as cp:
        yield cp()
        del cp().sent


@pytest.fixture(autouse=True)
def domain_event_publisher(containers):
    with containers.domain_event_publisher.override(FakeDomainEventPublisher()) as dep:
        yield dep()
        del dep().published


@pytest.fixture
def document_type_id() -> str:
    return uuid4().hex


@pytest.fixture
def tenant_id() -> str:
    return uuid4().hex


@pytest.fixture
def validation_result_id() -> str:
    return uuid4().hex


@pytest.fixture
def empty_validation_result(validation_result_id, tenant_id):
    return ValidationResult(id=validation_result_id, tenant_id=tenant_id, issues=[])


register(DocumentTypeFactory)
register(IssuesFactory)
register(ValidationResultFactory)
register(IssueFactory)
register(ExternalValidatorFactory)
register(RuleFactory)
register(CrossFieldIssueMessageFactory)
register(CrossFieldValidatorFactory)
