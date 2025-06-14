from enum import Enum

# region: aws-cdk
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_rds import DatabaseInstance

from aws_cdk.aws_cloudwatch import ComparisonOperator
# endregion

# region: origen cdk-pug-platform
from cdk_pug_platform.packages.application_monitoring.infrastructure import (
    TrackableService
)


from cdk_pug_platform.models.alarms import (
    AlarmCpuThresholds,
    AlarmMemoryThresholds,
    AlarmFreeStorageThresholds,
    AlarmFreeMemoryThresholds,
    AlarmIopsThresholds
)

from cdk_pug_platform.models.tenants.tenant_base import TenantBase
# endregion


class TrackableServicesBuilder:
    def _build_trackable_services(
            self,
            tenant: TenantBase,
            services: dict[
                Enum,
                ApplicationLoadBalancedFargateService
            ],
            databases: dict[Enum, DatabaseInstance]
    ):
        trackable_services = []
        for service, service_instance in services.items():
            trackable_services.extend([
                TrackableService(
                    service,
                    service_instance.
                    service.
                    metric_cpu_utilization(),
                    AlarmCpuThresholds.DANGER,
                ),
                TrackableService(
                    service,
                    service_instance.
                    service.
                    metric_cpu_utilization(),
                    AlarmCpuThresholds.set_warning_threshold(
                        tenant.ecs_fargate_blueprints[service].
                        scaling_rule.trigger_percent_cpu
                    ),
                ),
                TrackableService(
                    service,
                    service_instance.
                    service.
                    metric_memory_utilization(),
                    AlarmMemoryThresholds.DANGER,
                ),
                TrackableService(
                    service,
                    service_instance.
                    service.
                    metric_memory_utilization(),
                    AlarmMemoryThresholds.set_warning_threshold(
                        tenant.ecs_fargate_blueprints[service]
                        .scaling_rule.trigger_percent_memory
                    )
                )
            ]
            )

        db_trackable_services = []
        for service, db_instance in databases.items():

            AlarmIopsThresholds.set_threshold(
                tenant.rds_blueprints[service].capacity.iops
            )

            db_trackable_services.extend([
                TrackableService(
                    service,
                    db_instance.
                    metric_cpu_utilization(),
                    AlarmCpuThresholds.DANGER,
                ),
                TrackableService(
                    service,
                    db_instance.
                    metric_cpu_utilization(),
                    AlarmCpuThresholds.WARNING,
                ),
                TrackableService(
                    service,
                    db_instance.
                    metric_free_storage_space(),
                    AlarmFreeStorageThresholds.DANGER,
                    comparison_operator=ComparisonOperator.LESS_THAN_THRESHOLD
                ),
                TrackableService(
                    service,
                    db_instance.
                    metric_free_storage_space(),
                    AlarmFreeStorageThresholds.WARNING,
                    comparison_operator=ComparisonOperator.LESS_THAN_THRESHOLD
                ),
                TrackableService(
                    service,
                    db_instance.metric_freeable_memory(),
                    AlarmFreeMemoryThresholds.WARNING,
                    comparison_operator=ComparisonOperator.LESS_THAN_THRESHOLD
                ),
                TrackableService(
                    service,
                    db_instance.metric_freeable_memory(),
                    AlarmFreeMemoryThresholds.DANGER,
                    comparison_operator=ComparisonOperator.LESS_THAN_THRESHOLD
                ),
                TrackableService(
                    service,
                    db_instance.metric_read_iops(),
                    AlarmIopsThresholds.WARNING
                ),
                TrackableService(
                    service,
                    db_instance.metric_read_iops(),
                    AlarmIopsThresholds.DANGER
                ),
                TrackableService(
                    service,
                    db_instance.metric_write_iops(),
                    AlarmIopsThresholds.WARNING
                ),
                TrackableService(
                    service,
                    db_instance.metric_write_iops(),
                    AlarmIopsThresholds.DANGER
                )
            ])

        self.trackable_services = trackable_services + db_trackable_services
