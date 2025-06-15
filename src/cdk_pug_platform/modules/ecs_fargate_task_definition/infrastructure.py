# region: primitives
from enum import Enum
from typing import Optional
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import (
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_secretsmanager as secretsmanager,
    aws_efs as efs,
    aws_logs as logs,
)

# endregion

# region morales cdk-pug-platform
from cdk_pug_platform.models.containers.registry_types import RegistryTypes
from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.packages.secrets.parsers import (
    parse_secrets_for_ecs,
    parse_database_secret_for_ecs,
)
from cdk_pug_platform.packages.secrets.names import DB_PASS, DB_USER

# endregion


class LogGroupParams:
    log_group: logs.LogGroup
    log_group_name: str

    def __init__(self, log_group: logs.LogGroup, log_group_name: str) -> None:
        self.log_group = log_group
        self.log_group_name = log_group_name


class FileSystemParams:
    file_system: efs.FileSystem
    container_path: str
    read_only: bool

    def __init__(
        self,
        file_system: efs.FileSystem,
        container_path: Optional[str],
        read_only: bool,
    ) -> None:
        self.file_system = file_system
        self.container_path = container_path or "/mnt/efs"
        self.read_only = read_only


class EcsFargateTaskDefinitionParams:
    service_type: Enum
    container_image: ecs.ContainerImage
    registry_type: RegistryTypes
    service_secret: secretsmanager.Secret
    service_secret_names: type[Enum]
    log_group_params: LogGroupParams
    service_environment: dict = {}
    service_db_secret: Optional[secretsmanager.Secret] = None
    ecr_registry: Optional[ecr.Repository] = None
    file_system_params: Optional[FileSystemParams] = None

    def __init__(
        self,
        service_type: Enum,
        container_image: ecs.ContainerImage,
        registry_type: RegistryTypes,
        cpu_architecture: ecs.CpuArchitecture,
        service_secret: secretsmanager.Secret,
        service_secret_names: type[Enum],
        log_group_params: LogGroupParams,
        service_environment: Optional[dict[str, str]] = {},
        service_db_secret: Optional[secretsmanager.Secret] = None,
        ecr_registry: Optional[ecr.Repository] = None,
        file_system_params: Optional[FileSystemParams] = None,
    ) -> None:
        self.service_type = service_type
        self.registry_type = registry_type
        self.cpu_architecture = cpu_architecture
        self.container_image = container_image
        self.service_db_secret = service_db_secret
        self.service_secret = service_secret
        self.service_secret_names = service_secret_names
        self.service_environment = service_environment or {}
        self.log_group_params = log_group_params
        if registry_type == RegistryTypes.ECR and ecr_registry is None:
            raise ValueError("ECR registry is not initialized")
        self.ecr_registry = ecr_registry
        self.file_system_params = file_system_params


class EcsFargateTaskDefinitionPug(PugModule[ecs.FargateTaskDefinition]):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        params: EcsFargateTaskDefinitionParams,
    ) -> None:
        TASK_DEFINITION_SUFFIX = f"{params.service_type.value}-task-definition"
        TASK_DEFINITION_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-{TASK_DEFINITION_SUFFIX}"
        )

        task_definition = ecs.FargateTaskDefinition(
            scope,
            TASK_DEFINITION_NAME,
            family=TASK_DEFINITION_NAME,
            memory_limit_mib=tenant.ecs_fargate_blueprints[
                params.service_type
            ].compute.memory_limit_mib,
            cpu=tenant.ecs_fargate_blueprints[params.service_type].compute.cpu,
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=params.cpu_architecture,
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
            ),
        )

        CONTAINER_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-api-container"

        secrets = parse_secrets_for_ecs(params.service_secret, params.service_secret_names)  # type: ignore

        if params.service_db_secret:
            db_secrets = parse_database_secret_for_ecs(params.service_db_secret, DB_USER, DB_PASS)  # type: ignore
            secrets.update(db_secrets)

        DB_COMMAND_TIMEOUT = tenant.ecs_fargate_blueprints[
            params.service_type
        ].time_configuration.db_command_timeout_seconds

        params.service_environment.update(
            {
                "DB_COMMAND_TIMEOUT": str(DB_COMMAND_TIMEOUT),
                "ENVIRONMENT": tenant.ENVIRONMENT.value,
            }
        )

        if params.file_system_params:
            task_definition.add_volume(
                name=params.file_system_params.file_system.node.id,
                efs_volume_configuration=ecs.EfsVolumeConfiguration(
                    file_system_id=params.file_system_params.file_system.file_system_id,
                    transit_encryption="ENABLED",
                ),
            )

        container = task_definition.add_container(
            CONTAINER_NAME,
            image=params.container_image,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=params.log_group_params.log_group_name,
                log_group=params.log_group_params.log_group,
            ),
            environment=params.service_environment,
            secrets=secrets,
            command=tenant.ecs_fargate_blueprints[params.service_type].command,
            entry_point=tenant.ecs_fargate_blueprints[params.service_type].entry_point,
        )

        container.add_port_mappings(ecs.PortMapping(container_port=80, host_port=80))

        if params.file_system_params:
            container.add_mount_points(
                ecs.MountPoint(
                    container_path=params.file_system_params.container_path,
                    source_volume=params.file_system_params.file_system.node.id,
                    read_only=params.file_system_params.read_only,
                )
            )

        if params.registry_type == RegistryTypes.ECR and params.ecr_registry:
            params.ecr_registry.grant_pull(task_definition.task_role)

        super().__init__(task_definition)
