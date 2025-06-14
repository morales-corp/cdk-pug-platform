from enum import Enum
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class ScalingRulesBuilder:
    @staticmethod
    def _build_scaling_rules(
            tenant: TenantBase,
            services: dict[
                Enum,
                ApplicationLoadBalancedFargateService
            ]):
        CPU_POLICY_NAME = "cpu-scaling"
        MEMORY_POLICY_NAME = "memory-scaling"

        for service, service_instance in services.items():
            api_scaling = (
                service_instance.
                service.
                auto_scale_task_count(
                    min_capacity=(
                        tenant.ecs_fargate_blueprints[service]
                        .scaling_rule.min_capacity
                    ),
                    max_capacity=(
                        tenant.ecs_fargate_blueprints[service]
                        .scaling_rule.max_capacity
                    )
                )
            )

            api_scaling.scale_on_cpu_utilization(
                CPU_POLICY_NAME,
                policy_name=CPU_POLICY_NAME,
                target_utilization_percent=(
                    tenant.ecs_fargate_blueprints[service]
                    .scaling_rule.trigger_percent_cpu
                )
            )

            api_scaling.scale_on_memory_utilization(
                MEMORY_POLICY_NAME,
                policy_name=MEMORY_POLICY_NAME,
                target_utilization_percent=(
                    tenant.ecs_fargate_blueprints[service]
                    .scaling_rule.trigger_percent_memory
                )
            )
