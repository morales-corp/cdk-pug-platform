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
    aws_applicationautoscaling as appscaling,
)

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.tenants.tenant_base import TenantBase

# endregion


# region: morales cdk-pug-platform -> ecs scheduled fargate task params


class EcsScheduledFargateTaskParams:
    service_type: Enum
    cluster: ecs.Cluster
    task_definition: ecs.FargateTaskDefinition
    subnet_type: ec2.SubnetType

    def __init__(
        self,
        service_type: Enum,
        cluster: ecs.Cluster,
        task_definition: ecs.FargateTaskDefinition,
        subnet_type: Optional[ec2.SubnetType] = None,
    ) -> None:
        self.service_type = service_type
        self.cluster = cluster
        self.task_definition = task_definition
        self.subnet_type = subnet_type or ec2.SubnetType.PRIVATE_WITH_EGRESS


# endregion


class EcsScheduledFargateTaskPug(PugModule[ecs_patterns.ScheduledFargateTask]):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        params: EcsScheduledFargateTaskParams,
    ):
        ECS_SCHEDULED_TASK_NAME = (
            f"{tenant.COMPANY}-"
            f"{tenant.ENVIRONMENT.value}-"
            f"{params.service_type.value}-scheduled-task"
        )

        scheduled_task = ecs_patterns.ScheduledFargateTask(
            scope,
            ECS_SCHEDULED_TASK_NAME,
            rule_name=ECS_SCHEDULED_TASK_NAME,
            schedule=appscaling.Schedule.expression(
                tenant.ecs_fargate_blueprints[params.service_type].schedule
            ),
            cluster=params.cluster,
            desired_task_count=tenant.ecs_fargate_blueprints[
                params.service_type
            ].desired_task_count,
            platform_version=ecs.FargatePlatformVersion.LATEST,
            subnet_selection=ec2.SubnetSelection(subnet_type=params.subnet_type),
            propagate_tags=ecs.PropagatedTagSource.TASK_DEFINITION,
            scheduled_fargate_task_definition_options={
                "task_definition": params.task_definition
            },
        )

        super().__init__(scheduled_task)
