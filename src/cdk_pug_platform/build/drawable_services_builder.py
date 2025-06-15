from enum import Enum

# region: aws-cdk
from aws_cdk.aws_elasticloadbalancingv2 import HttpCodeElb
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_rds import DatabaseInstance
# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.monitoring.colors import Colors
from cdk_pug_platform.packages.application_dashboard.infrastructure import (
    DrawableService,
)
# endregion


class DrawableServicesBuilder:
    def _build_drawable_services(
            self,
            services: dict[
                Enum,
                ApplicationLoadBalancedFargateService
            ],
            log_groups: dict[Enum, LogGroup],
            databases: dict[Enum, DatabaseInstance]
    ):
        self.drawable_services = []
        for service, service_instance in services.items():
            self.drawable_services.extend([
                DrawableService(
                    service,
                    [
                        service_instance.
                        load_balancer.
                        metric_request_count(
                            color=Colors.REQUEST_COUNT_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_target_response_time(
                            color=Colors.RESPONSE_TIME_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_active_connection_count(
                            color=Colors.ACTIVE_CONNECTION_COUNT_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_new_connection_count(
                            color=Colors.NEW_CONNECTION_COUNT_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_processed_bytes(
                            color=Colors.PROCESSED_BYTES_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_http_code_elb(
                            code=HttpCodeElb.ELB_5XX_COUNT,
                            color=Colors.HTTP_CODE_ELB_5XX_COUNT_COLOR
                        ),
                        service_instance.
                        load_balancer.
                        metric_http_code_elb(
                            code=HttpCodeElb.ELB_4XX_COUNT,
                            color=Colors.HTTP_CODE_ELB_4XX_COUNT_COLOR
                        ),
                        service_instance.
                        service.
                        metric_cpu_utilization(
                            color=Colors.CPU_UTILIZATION_COLOR
                        ),
                        service_instance.
                        service.
                        metric_memory_utilization(
                            color=Colors.MEMORY_UTILIZATION_COLOR
                        )
                    ],
                    log_groups.get(service)
                )
            ])

        for service, db_instance in databases.items():
            self.drawable_services.extend([
                DrawableService(
                    service,
                    [
                        db_instance.
                        metric_cpu_utilization(
                            color=Colors.CPU_UTILIZATION_COLOR
                        ),
                        db_instance.
                        metric_free_storage_space(
                            color=Colors.FREE_STORAGE_SPACE_COLOR
                        ),
                        db_instance.
                        metric_freeable_memory(
                            color=Colors.FREEABLE_MEMORY_COLOR
                        ),
                        db_instance.
                        metric_read_iops(
                            color=Colors.READ_IOPS_COLOR
                        ),
                        db_instance.
                        metric_write_iops(
                            color=Colors.WRITE_IOPS_COLOR
                        )
                    ]
                )
            ])
