# region: primitives
from enum import Enum
from constructs import Construct
from typing import Optional, Sequence
# endregion

# region: aws-cdk
from aws_cdk.aws_secretsmanager import Secret, ISecret
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_ecs import CpuArchitecture
# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.modules.ecr_registry.infrastructure import EcrRegistryPug
from cdk_pug_platform.modules.container_image.infrastructure import (
    RegistryTypes,
    ContainerImageParams,
    ContainerImagePug
)
from cdk_pug_platform.modules.logs.log_group.infrastructure import LogGroupPug
from cdk_pug_platform.modules.ecs_fargate_task_definition.infrastructure import (
    LogGroupParams,
    EcsFargateTaskDefinitionParams,
    EcsFargateTaskDefinitionPug,
    FileSystemParams
)

# endregion


class _Amd64Architecture:
    def __init__(self):
        self.cpu_architecture = CpuArchitecture.X86_64
        self.platform = Platform.LINUX_AMD64


class _Arm64Architecture:
    def __init__(self):
        self.cpu_architecture = CpuArchitecture.ARM64
        self.platform = Platform.LINUX_ARM64


class EcsComputeArchitecture(Enum):
    """
    EcsComputeArchitecture Enum
    ===========================

    This enum defines supported compute architectures for Amazon ECS Fargate.

    ## Architectures
    ### AMD64 (`_Amd64Architecture`)
    - Standard x86_64 architecture CISC (Complex Instruction Set Computing).
    - High compatibility with legacy applications and most container images.
    - Higher power consumption but optimized for performance-intensive workloads.
    - Preferred for general-purpose compute tasks.

    ### ARM64 (`_Arm64Architecture`)
    - Energy-efficient RISC-based (Reduced Instruction Set Computing) architecture.
    - Optimized for cloud-native workloads on AWS Graviton (Fargate), Apple Silicon, and Ampere.
    - Lower power consumption, reducing costs for long-running services.
    - Well-suited for microservices and highly parallel workloads.

    ## Cloud & Container Use Cases
    - **AMD64**: Best for compute-heavy applications with broad compatibility.
    - **ARM64**: Ideal for cost-efficient, high-performance cloud-native services.

    ## Policy
    - Is mandatory for all ECS Fargate services to specify the compute architecture.
    - The default architecture is `ARM64` for cost savings and performance efficiency.
    - Container images must be compatible with the selected architecture E.g:
        - *-bookworm-slim-arm64v8 for ARM64: Ensuring compatibility and efficiency.
        - *-bookworm-slim-amd64 for AMD64: Enhancing performance and compatibility.

    ## Example Usage
    ```python
    selected_arch = EcsComputeArchitecture.ARM64.value
    print(selected_arch.cpu_architecture)  # ARM64
    print(selected_arch.platform)  # LINUX_ARM64
    """
    AMD64 = _Amd64Architecture()
    ARM64 = _Arm64Architecture()


class ServiceTaskDefinitionBuilder(Construct):
    def _build_task_definition(
        self,
        tenant: TenantBase,
        service_type: Enum,
        registry_type: RegistryTypes,
        service_secret: Secret,
        container_secret_names: type[Enum],
        ecs_compute_architecture: EcsComputeArchitecture,
        service_db_secret: Optional[Secret] = None,
        registry_credentials: Optional[ISecret] = None,
        image_uri: Optional[str] = None,
        file_system_params: Optional[FileSystemParams] = None,
        relative_path: Optional[str] = None,
        file: Optional[str] = None,
        exclude: Optional[Sequence[str]] = None,
        service_environment: Optional[dict[str, str]] = None,
        ecr_registry: Optional[Repository] = None,
    ):
        if registry_type == RegistryTypes.ECR and not ecr_registry:
            self.ecr_registry = EcrRegistryPug(
                self,
                tenant,
                service_type
            ).play()
        elif registry_type == RegistryTypes.ECR and ecr_registry:
            self.ecr_registry = ecr_registry
        else:
            self.ecr_registry = None

        container_image_params = ContainerImageParams(
            service_type=service_type,
            registry_type=registry_type,
            platform=ecs_compute_architecture.value.platform,
            credentials=registry_credentials,
            image_uri=image_uri,
            ecr_registry=self.ecr_registry,
            relative_path=relative_path,
            file=file,
            exclude=exclude
        )

        self.container_image = ContainerImagePug(container_image_params).play()

        self.log_group = LogGroupPug(
            self,
            tenant,
            service_type
        ).play()

        log_group_params = LogGroupParams(
            log_group=self.log_group,
            log_group_name=self.log_group.log_group_name
        )

        task_definition_params = EcsFargateTaskDefinitionParams(
            service_type=service_type,
            container_image=self.container_image,
            registry_type=registry_type,
            cpu_architecture=ecs_compute_architecture.value.cpu_architecture,
            ecr_registry=self.ecr_registry,
            service_db_secret=service_db_secret,
            service_secret=service_secret,
            service_secret_names=container_secret_names,
            log_group_params=log_group_params,
            service_environment=service_environment,
            file_system_params=file_system_params
        )

        self.task_definition = EcsFargateTaskDefinitionPug(
            self,
            tenant,
            task_definition_params
        ).play()
