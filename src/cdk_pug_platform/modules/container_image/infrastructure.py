# region: primitives
from enum import Enum
from typing import Optional, Sequence

# endregion

# region: aws-cdk
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ecr_assets as ecr_assets,
    aws_secretsmanager as secretsmanager,
)

# endregion

# region morales cdk-pug-platform
from cdk_pug_platform.models.containers.registry_types import RegistryTypes
from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.utils.configs import DeploymentConfig

# endregion


class ContainerImageParams:
    service_type: Enum
    registry_type: RegistryTypes
    image_name: Optional[str] = None
    image_tag: Optional[str] = None
    image_uri: Optional[str] = None
    ecr_registry: Optional[ecr.Repository] = None
    credentials: Optional[secretsmanager.ISecret] = None
    relative_path: Optional[str] = None
    file: Optional[str] = None
    exclude: Optional[Sequence[str]] = None

    def __init__(
        self,
        service_type: Enum,
        registry_type: RegistryTypes,
        platform: ecr_assets.Platform,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        image_uri: Optional[str] = None,
        ecr_registry: Optional[ecr.Repository] = None,
        credentials: Optional[secretsmanager.ISecret] = None,
        relative_path: Optional[str] = None,
        file: Optional[str] = None,
        exclude: Optional[Sequence[str]] = None,
    ) -> None:
        self.service_type = service_type
        self.registry_type = registry_type
        self.platform = platform
        self.image_name = image_name
        self.image_tag = image_tag
        self.image_uri = image_uri
        self.ecr_registry = ecr_registry
        self.credentials = credentials
        self.is_first_deployment = DeploymentConfig.is_first_deployment()
        self.relative_path = relative_path
        self.file = file
        self.exclude = exclude


class ContainerImagePug(PugModule[ecs.ContainerImage]):
    def __init__(self, params: ContainerImageParams):
        if params.is_first_deployment and params.relative_path is not None:
            container_image = ecs.ContainerImage.from_asset(
                params.relative_path,
                file=params.file,
                exclude=params.exclude,
                platform=params.platform,
            )
        elif params.registry_type == RegistryTypes.ECR:
            if params.ecr_registry is None:
                raise ValueError("ECR registry is not initialized")
            if params.image_tag is None:
                params.image_tag = "latest"

            container_image = ecs.ContainerImage.from_ecr_repository(
                params.ecr_registry, tag=params.image_tag
            )
        elif params.registry_type == RegistryTypes.PRIVATE:
            if params.credentials is None:
                raise ValueError("Credentials are not initialized")
            if params.image_uri is None:
                raise ValueError("Image URI is not initialized")
            container_image = ecs.ContainerImage.from_registry(
                params.image_uri, credentials=params.credentials
            )
        else:
            if params.image_name is None:
                raise ValueError("Image name is not initialized")
            if params.image_tag is None:
                raise ValueError("Image tag is not initialized")
            container_image = ecs.ContainerImage.from_registry(
                f"{params.image_name}:{params.image_tag}"
            )

        super().__init__(container_image)
