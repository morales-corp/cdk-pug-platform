# region: primitives
from enum import Enum
from constructs import Construct
from typing import Optional, Sequence

# endregion

# region: aws-cdk
from aws_cdk import aws_ecs as ecs, aws_ec2 as ec2
from aws_cdk.aws_secretsmanager import ISecret

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.build.service_secrets_builder import ServiceSecretsBuilder
from cdk_pug_platform.build.service_task_definition_builder import (
    ServiceTaskDefinitionBuilder,
    RegistryTypes,
    FileSystemParams,
    EcsComputeArchitecture,
)
from cdk_pug_platform.modules.ecs_scheduled_fargate_task.infrastructure import (
    EcsScheduledFargateTaskParams,
    EcsScheduledFargateTaskPug,
)

# endregion


class EcsScheduledTask(ServiceSecretsBuilder, ServiceTaskDefinitionBuilder, Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        cluster: ecs.Cluster,
        service_type: Enum,
        registry_type: RegistryTypes,
        container_secret_names: type[Enum],
        ecs_compute_architecture: EcsComputeArchitecture,
        is_unique: bool = False,
        is_db_secret_required: bool = True,
        relative_path: Optional[str] = None,
        image_uri: Optional[str] = None,
        file: Optional[str] = None,
        exclude: Optional[Sequence[str]] = None,
        subnet_type: Optional[ec2.SubnetType] = None,
        service_environment: Optional[dict[str, str]] = None,
        registry_credentials: Optional[ISecret] = None,
        file_system_params: Optional[FileSystemParams] = None,
        **kwargs,
    ):
        CONSTRUCT_ID = (
            "ecs-scheduled-task"
            if is_unique
            else f"ecs-scheduled-task-{service_type.value}"
        )
        super().__init__(scope, CONSTRUCT_ID, **kwargs)

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

        scheduled_task_params = EcsScheduledFargateTaskParams(
            service_type=service_type,
            cluster=cluster,
            task_definition=self.task_definition,
            subnet_type=subnet_type,
        )

        self.scheduled_task = EcsScheduledFargateTaskPug(
            self, tenant, scheduled_task_params
        ).play()
