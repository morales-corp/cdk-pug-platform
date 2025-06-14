# region: primitives
from enum import Enum
from constructs import Construct
# endregion

# region: aws-cdk
from aws_cdk import (
    aws_secretsmanager as secretsmanager
)
# endregion

# region: origen cdk-pug-platform
from cdk_pug_platform.packages.secrets.parsers import parse_secrets_from_env
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
# endregion


class ServiceSecretsBuilder(Construct):
    def _build_service_secrets(
        self,
        tenant: TenantBase,
        service_type: Enum,
        secret_names: type[Enum],
        is_db_secret_required: bool = False
    ):
        SERVICE_SECRET_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-"
            f"{service_type.value}-service-secret"
        )

        self.service_secret = secretsmanager.Secret(
            self,
            SERVICE_SECRET_NAME,
            secret_name=SERVICE_SECRET_NAME,
            description=(
                f"Secret for {tenant.COMPANY} {tenant.ENVIRONMENT.value} "
                f"{service_type.value} service secret"
            ),
            secret_object_value=parse_secrets_from_env(
                tenant,
                service_type,
                secret_names
            )
        )

        self.service_db_secret = None
        if is_db_secret_required:
            SERVICE_DB_CREDENTIALS_SECRET_NAME = (
                f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-"
                f"{service_type.value}-db-credentials"
            )
            self.service_db_secret = secretsmanager.Secret(
                self,
                SERVICE_DB_CREDENTIALS_SECRET_NAME,
                secret_name=SERVICE_DB_CREDENTIALS_SECRET_NAME,
                description=(
                    f"Secret for {tenant.COMPANY} {tenant.ENVIRONMENT.value} "
                    f"{service_type.value} database credentials"
                )
            )
