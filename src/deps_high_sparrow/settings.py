from typing import Any

from deps_asb import ASBSettings
from deps_kafka import KafkaSettings
from deps_message_flow import MessagingDriverEnum
from deps_rabbitmq import RabbitMQTLSSettings
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from deps_high_sparrow.extras import DatabaseSettings, ServiceInfoSettings


class ExtractionProxySettings(BaseSettings):
    url: str
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="EXTRACTION_")


class ExternalValidationProxySettings(BaseSettings):
    timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="EXTERNAL_VALIDATION_")


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"

    logger_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    info: ServiceInfoSettings = ServiceInfoSettings()
    database: DatabaseSettings = DatabaseSettings()

    messaging_driver: MessagingDriverEnum = Field(MessagingDriverEnum.RABBITMQ, validation_alias="MESSAGING_DRIVER")
    messaging_driver_settings: Any = Field(None, validation_alias="MESSAGING_DRIVER_SETTINGS")
    message_broker_connection_string: str

    documentation_enabled: bool = True

    extraction: ExtractionProxySettings = ExtractionProxySettings()
    external_validation: ExternalValidationProxySettings = ExternalValidationProxySettings()

    ssl_verify: bool = False
    instrumentation_enabled: bool = False

    model_config = SettingsConfigDict(use_enum_values=True)

    @field_validator("messaging_driver_settings")
    @classmethod
    def validate_messaging_driver_settings(cls, v, info):  # noqa: N805
        messaging_driver = info.data.get("messaging_driver")
        if not messaging_driver:
            raise ValueError("Invalid messaging driver")

        driver = MessagingDriverEnum(messaging_driver)
        if driver == MessagingDriverEnum.ASB:
            return ASBSettings()
        elif driver == MessagingDriverEnum.KAFKA:
            return KafkaSettings()
        elif driver == MessagingDriverEnum.RABBITMQ:
            return RabbitMQTLSSettings().dict()  # TODO: use BaseSettings

        raise ValueError(f"Driver {driver} is not implemented")
