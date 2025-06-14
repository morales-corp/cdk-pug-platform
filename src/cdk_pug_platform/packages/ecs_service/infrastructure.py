from typing import Optional, Sequence

from constructs import Construct
from enum import Enum

from cdk_pug_platform.build.service_load_balancer_logging_builder import (
    ServiceLoadBalancerLoggingBuilder,
)
from cdk_pug_platform.build.service_secrets_builder import ServiceSecretsBuilder


from cdk_pug_platform.modules.ecs_fargate_service.infrastructure import (
    EcsFargateServiceParams,
    EcsFargateServicePug,
)

from aws_cdk import aws_ecs as ecs, aws_ec2 as ec2


from aws_cdk.aws_secretsmanager import ISecret

from cdk_pug_platform.packages.federated_dns.infrastructure import FederatedDns

from cdk_pug_platform.models.tenants.tenant_base import TenantBase


from cdk_pug_platform.build.service_task_definition_builder import (
    ServiceTaskDefinitionBuilder,
    RegistryTypes,
    FileSystemParams,
    EcsComputeArchitecture,
)


class EcsService(
    ServiceSecretsBuilder,
    ServiceTaskDefinitionBuilder,
    ServiceLoadBalancerLoggingBuilder,
    Construct,
):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        cluster: ecs.Cluster,
        service_type: Enum,
        registry_type: RegistryTypes,
        container_secret_names: type[Enum],
        ecs_compute_architecture: EcsComputeArchitecture,
        tenant_dns: FederatedDns,
        is_unique: bool = False,
        is_db_secret_required: bool = True,
        relative_path: Optional[str] = None,
        image_uri: Optional[str] = None,
        file: Optional[str] = None,
        exclude: Optional[Sequence[str]] = None,
        is_internal: Optional[bool] = False,
        subnet_type: Optional[ec2.SubnetType] = None,
        service_environment: Optional[dict[str, str]] = None,
        registry_credentials: Optional[ISecret] = None,
        file_system_params: Optional[FileSystemParams] = None,
    ):
        CONSTRUCT_ID = (
            "ecs-service" if is_unique else f"ecs-service-{service_type.value}"
        )
        super().__init__(scope, CONSTRUCT_ID)

        if is_unique:
            self._build_load_balancer_logging(tenant)

        self._build_service_secrets(
            tenant, service_type, container_secret_names, is_db_secret_required
        )

        self._build_task_definition(
            tenant,
            service_type,
            registry_type,
            self.service_secret,
            container_secret_names,
            ecs_compute_architecture,
            self.service_db_secret,
            registry_credentials,
            image_uri,
            file_system_params,
            relative_path,
            file,
            exclude,
            service_environment,
        )

        service_params = EcsFargateServiceParams(
            service_type=service_type,
            cluster=cluster,
            task_definition=self.task_definition,
            is_internal=is_internal if is_internal else False,
            certificate=None if is_internal else tenant_dns.certificate,
            public_hosted_zone=tenant_dns.main_zone,
            private_hosted_zone=tenant_dns.private_zone,
            subnet_type=subnet_type,
        )

        self.service = EcsFargateServicePug(self, tenant, service_params).play()

        if is_unique:
            self._build_log_access_logs(self.service.load_balancer, service_type.value)
