from constructs import Construct


from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
)

from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class EcsCluster(Construct):
    def __init__(
        self, scope: Construct, tenant: TenantBase, tenant_vpc: ec2.Vpc, **kwargs
    ):
        super().__init__(scope, "ecs-cluster", **kwargs)

        ECS_CLUSTER_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-ecs-cluster"
        self.tenant_ecs_cluster = ecs.Cluster(
            self,
            ECS_CLUSTER_NAME,
            cluster_name=ECS_CLUSTER_NAME,
            vpc=tenant_vpc,
            container_insights=True,
        )
