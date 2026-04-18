from typing import Any, Dict, Optional, Type, Union

from dependency_injector import containers, providers, resources
from deps_asb import ASBClient, ASBConsumer, ASBProducer
from deps_kafka import KafkaClient, KafkaConsumer, KafkaProducer
from deps_message_flow import MessagingDriverEnum
from deps_message_flow.commands.producer import CommandProducer
from deps_message_flow.events.publisher import DomainEventPublisher
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer
from deps_rabbitmq import RabbitMQClient, RabbitMQConsumer, RabbitMQProducer

from deps_high_sparrow.application import (
    DocumentTypeService,
    ExternalValidationService,
    IExternalValidationProxy,
    IExtractionProxy,
    RuleService,
    ValidationResultService,
    ValidatorService,
)
from deps_high_sparrow.constants import PROJECT_NAME
from deps_high_sparrow.domain.model import (
    IDocumentTypeRepository,
    IValidationResultRepository,
)
from deps_high_sparrow.extras import Database, DBDialect, DBDriver
from deps_high_sparrow.infrastructure.proxies import (
    ExternalValidationProxy,
    ExtractionProxy,
)
from deps_high_sparrow.infrastructure.repositories import (
    DocumentTypeRepository,
    ValidationResultRepository,
)
from deps_high_sparrow.messaging.dispatcher import make_message_dispatcher

MessagingClient = Union[ASBClient, KafkaClient, RabbitMQClient]


class DatabaseResource(resources.Resource):
    def init(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        dialect: DBDialect,
        driver: DBDriver,
        require_secure_transport: bool,
    ) -> Database:
        db = Database(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            dialect=dialect,
            driver=driver,
            require_secure_transport=require_secure_transport,
        )
        db.connect()
        return db

    def shutdown(self, resource: Database) -> None:
        resource.close()


class MessageBrokerResource(resources.Resource):
    def init(
        self,
        driver_type: str,
        expected_driver: str,
        client: Type[MessagingClient],
        message_connection_string: str,
        **kwargs: Dict[str, Any],
    ) -> Optional[MessagingClient]:
        return client(message_connection_string, **kwargs) if driver_type == expected_driver else None

    def shutdown(self, resource: Optional[MessagingClient]) -> None:
        if resource:
            resource.close()


class MessageBrokers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    broker_client: providers.Provider[MessagingClient] = providers.Selector(
        config.messaging_driver,
        asb=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.ASB.value,
            expected_driver=config.messaging_driver,
            client=ASBClient,
            message_connection_string=config.message_broker_connection_string,
            asb_settings=messaging_driver_settings,
        ),
        kafka=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.KAFKA.value,
            expected_driver=config.messaging_driver,
            client=KafkaClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
        rabbitmq=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.RABBITMQ.value,
            expected_driver=config.messaging_driver,
            client=RabbitMQClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
    )


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()
    message_brokers = providers.DependenciesContainer()

    producer: providers.Provider[IMessageProducer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBProducer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
        ),
        kafka=providers.Singleton(
            KafkaProducer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQProducer,
            client=message_brokers.broker_client,
        ),
    )
    consumer: providers.Provider[IMessageConsumer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBConsumer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
            custom_subscription_name=PROJECT_NAME,
        ),
        kafka=providers.Singleton(
            KafkaConsumer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQConsumer,
            client=message_brokers.broker_client,
        ),
    )


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    build_info: providers.Provider[Dict] = providers.Dict(
        {
            "build_tag": config.info.tag,
            "build_date": config.info.date,
            "commit_hash": config.info.hash,
        },
    )


class Datasources(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_datasource: providers.Provider[Database] = providers.Resource(
        DatabaseResource,
        config.user,
        config.password,
        config.host,
        config.port,
        config.db,
        config.dialect,
        config.driver,
        config.require_secure_transport,
    )


class Repositories(containers.DeclarativeContainer):
    datasources = providers.DependenciesContainer()

    document_type: providers.Singleton[IDocumentTypeRepository] = providers.Singleton(
        DocumentTypeRepository,
        database=datasources.postgres_datasource,
    )
    validation_result: providers.Singleton[IValidationResultRepository] = providers.Singleton(
        ValidationResultRepository,
        database=datasources.postgres_datasource,
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    extraction: providers.Singleton[IExtractionProxy] = providers.Singleton(
        ExtractionProxy,
        base_url=config.extraction.url,
        timeout=config.extraction.timeout,
        ssl_verify=config.ssl_verify,
    )
    external_validation: providers.Singleton[IExternalValidationProxy] = providers.Singleton(
        ExternalValidationProxy,
        timeout=config.external_validation.timeout,
        ssl_verify=config.ssl_verify,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    command_producer: CommandProducer = providers.Dependency()
    external_services = providers.DependenciesContainer()
    domain_event_publisher: DomainEventPublisher = providers.Dependency()

    rule: providers.Singleton[RuleService] = providers.Singleton(
        RuleService,
        document_type_repository=repositories.document_type,
    )

    document_type: providers.Singleton[DocumentTypeService] = providers.Singleton(
        DocumentTypeService,
        document_type_repository=repositories.document_type,
        command_producer=command_producer,
    )

    external_validation: providers.Singleton[ExternalValidationService] = providers.Singleton(
        ExternalValidationService,
        external_validation_proxy=external_services.external_validation,
    )

    validation_result: providers.Singleton[ValidationResultService] = providers.Singleton(
        ValidationResultService,
        validation_result_repository=repositories.validation_result,
        extraction_proxy=external_services.extraction,
        external_validation_service=external_validation,
        document_type_repository=repositories.document_type,
        domain_event_publisher=domain_event_publisher,
    )

    validator: providers.Singleton[ValidatorService] = providers.Singleton(
        ValidatorService,
        document_type_repository=repositories.document_type,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    datasources: providers.Container[Datasources] = providers.Container(
        Datasources,
        config=config.database,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        datasources=datasources,
    )

    core: providers.Container[Core] = providers.Container(Core, config=config)
    message_brokers: providers.Container[MessageBrokers] = providers.Container(
        MessageBrokers,
        config=config,
        messaging_driver_settings=messaging_driver_settings,
    )

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
        message_brokers=message_brokers,
    )

    command_producer: providers.Singleton[CommandProducer] = providers.Singleton(
        CommandProducer,
        messaging.producer,
    )

    domain_event_publisher: providers.Singleton[DomainEventPublisher] = providers.Singleton(
        DomainEventPublisher,
        messaging.producer,
    )

    message_dispatcher: providers.Singleton[IMessageConsumer] = providers.Singleton(
        make_message_dispatcher,
        messaging.consumer,
        messaging.producer,
    )

    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )

    application: providers.Container[Application] = providers.Container(
        Application,
        config=config,
        repositories=repositories,
        command_producer=command_producer,
        external_services=external_services,
        domain_event_publisher=domain_event_publisher,
    )
