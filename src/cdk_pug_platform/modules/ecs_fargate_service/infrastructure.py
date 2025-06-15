# region: primitives
from enum import Enum
from typing import Optional
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_certificatemanager as acm,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
)

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.environments.app_environment import AppEnvironment
from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.tenants.tenant_base import TenantBase

# endregion

# region: morales cdk-pug-platform -> ecs fargate service params


class EcsFargateServiceParams:
    service_type: Enum
    cluster: ecs.Cluster
    task_definition: ecs.FargateTaskDefinition
    is_internal: bool
    subnet_type: ec2.SubnetType
    public_hosted_zone: Optional[route53.IHostedZone]
    private_hosted_zone: Optional[route53.PrivateHostedZone]
    certificate: Optional[acm.ICertificate]

    def __init__(
        self,
        service_type: Enum,
        cluster: ecs.Cluster,
        task_definition: ecs.FargateTaskDefinition,
        is_internal: bool,
        subnet_type: Optional[ec2.SubnetType] = None,
        public_hosted_zone: Optional[route53.IHostedZone] = None,
        private_hosted_zone: Optional[route53.PrivateHostedZone] = None,
        certificate: Optional[acm.ICertificate] = None,
    ) -> None:
        self.service_type = service_type
        self.cluster = cluster
        self.task_definition = task_definition
        self.is_internal = is_internal
        self.public_hosted_zone = public_hosted_zone
        self.private_hosted_zone = private_hosted_zone
        self.certificate = certificate
        self.subnet_type = subnet_type or ec2.SubnetType.PRIVATE_WITH_EGRESS


# endregion


class EcsFargateServicePug(
    PugModule[ecs_patterns.ApplicationLoadBalancedFargateService]
):
    def __init__(
        self, scope: Construct, tenant: TenantBase, params: EcsFargateServiceParams
    ):
        ECS_SERVICE_NAME = (
            f"{tenant.COMPANY}-"
            f"{tenant.ENVIRONMENT.value}-{params.service_type.value}-container-service"
        )

        container_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            scope,
            ECS_SERVICE_NAME,
            service_name=ECS_SERVICE_NAME,
            cluster=params.cluster,
            task_definition=params.task_definition,
            listener_port=80 if params.is_internal else 443,
            redirect_http=False if params.is_internal else True,
            public_load_balancer=False if params.is_internal else True,
            certificate=None if params.is_internal else params.certificate,
            domain_zone=(
                params.private_hosted_zone
                if params.is_internal
                else params.public_hosted_zone
            ),
            domain_name=(
                params.service_type.value
                if tenant.ENVIRONMENT == AppEnvironment.LIVE
                else f"{params.service_type.value}-{tenant.ENVIRONMENT.value}"
            ),
            protocol=(
                elbv2.ApplicationProtocol.HTTP
                if params.is_internal
                else elbv2.ApplicationProtocol.HTTPS
            ),
            task_subnets=ec2.SubnetSelection(subnet_type=params.subnet_type),
            assign_public_ip=(
                True if params.subnet_type == ec2.SubnetType.PUBLIC else False
            ),
            idle_timeout=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.load_balancer_timeout,
            platform_version=ecs.FargatePlatformVersion.LATEST,
            propagate_tags=ecs.PropagatedTagSource.TASK_DEFINITION,
            enable_ecs_managed_tags=True,
        )

        container_service.target_group.configure_health_check(
            path=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.health_path,
            healthy_http_codes=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.healthy_http_codes,
            interval=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.health_check_interval,
            timeout=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.health_check_timeout,
            healthy_threshold_count=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.healthy_threshold_count,
            unhealthy_threshold_count=tenant.ecs_fargate_blueprints[
                params.service_type
            ].time_configuration.unhealthy_threshold_count,
        )

        super().__init__(container_service)
