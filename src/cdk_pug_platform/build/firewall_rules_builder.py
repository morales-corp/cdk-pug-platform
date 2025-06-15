from enum import Enum
from typing import Optional

# region aws_cdk
from aws_cdk.aws_ecs_patterns import (
    ApplicationLoadBalancedFargateService,
    ScheduledFargateTask
)
from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_ec2 import Port, PrefixList, Peer, SecurityGroup
# endregion

from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.models.environments.app_environment import AppEnvironment


class FirewallRulesBuilder:
    @staticmethod
    def _build_firewall_rules(
            tenant: TenantBase,
            services: dict[
                Enum,
                ApplicationLoadBalancedFargateService
            ],
            databases: dict[Enum, DatabaseInstance],
            prefix_list: PrefixList,
            scheduled_tasks: Optional[dict[Enum, ScheduledFargateTask]] = None,
            power_bi_bastion_security_group: Optional[SecurityGroup] = None
    ):
        for database, database_instance in databases.items():
            port = Port.tcp(database_instance.instance_endpoint.port)
            for security_group in (
                    database_instance.connections.security_groups):
                security_group.add_ingress_rule(
                    peer=Peer.prefix_list(
                        prefix_list.prefix_list_id),
                    connection=port,
                    description=(
                        "Allow DATABASE access from morales Corp CIDR"
                    )
                )
                for service, service_instance in services.items():
                    (
                        service_instance.
                        service.
                        connections.
                        allow_to(
                            security_group,
                            port,
                            (f"Allow {service.name} container to connect "
                             "to database")
                        )
                    )
                if scheduled_tasks:
                    for scheduled_task, scheduled_task_instance in scheduled_tasks.items():
                        if scheduled_task_instance.task.security_groups:
                            for task_security_group in scheduled_task_instance.task.security_groups:
                                security_group.add_ingress_rule(
                                    peer=task_security_group,
                                    connection=port,
                                    description=(
                                        f"Allow {scheduled_task.name} container to connect "
                                        "to database")
                                )
                if tenant.ENVIRONMENT == AppEnvironment.LIVE:
                    security_group.add_ingress_rule(
                        peer=power_bi_bastion_security_group,
                        connection=port,
                        description=(
                            "Allow Power BI Bastion to connect to database")
                    )
