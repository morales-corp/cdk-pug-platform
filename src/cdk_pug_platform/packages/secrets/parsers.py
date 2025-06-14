import os
from enum import Enum
import aws_cdk as core
from aws_cdk import (
    aws_secretsmanager as secretsmanager,
    aws_ecs as ecs,
)

from typing import Optional

from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.utils.validators.environment_validator import EnvironmentValidator
from cdk_pug_platform.utils.configs import PathConfig


def parse_secrets_from_env(
    tenant: TenantBase,
    service_type: Enum,
    secret_names: type[Enum],
) -> dict[str, core.SecretValue] | None:
    env_path = (
        f"{PathConfig.get_folder_environment_config_path()}/"
        f"{tenant.ENVIRONMENT.value}/{service_type.value}.env"
    )
    EnvironmentValidator.validate(env_path)
    environment_json: dict[str, core.SecretValue] = {}

    for secret_name in secret_names:
        secret_value = os.getenv(secret_name.value)
        if secret_value is None:
            raise Exception(f"Secret not found in environment: {secret_name.value}")
        environment_json[secret_name.value] = core.SecretValue.plain_text(secret_value)

    return environment_json


def parse_secrets_for_ecs(
    secret: secretsmanager.ISecret, secret_names: type[Enum]
) -> dict[str, ecs.Secret]:
    return {
        secret_name.value: ecs.Secret.from_secrets_manager(secret, secret_name.value)
        for secret_name in secret_names
    }


def parse_database_secret_for_ecs(
    secret: secretsmanager.ISecret, user_key: Optional[str], pass_key: Optional[str]
):
    if user_key is not None and pass_key is not None:
        parsed_secret = {
            user_key: ecs.Secret.from_secrets_manager(secret, "username"),
            pass_key: ecs.Secret.from_secrets_manager(secret, "password"),
        }
    else:
        parsed_secret = {
            "ConnectionString": ecs.Secret.from_secrets_manager(
                secret, "ConnectionString"
            )
        }

    return parsed_secret
