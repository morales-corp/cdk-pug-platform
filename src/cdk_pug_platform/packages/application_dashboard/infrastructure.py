from enum import Enum
from constructs import Construct

from aws_cdk import (
    Aws,
    CfnOutput,
    aws_cloudwatch as cloudwatch,
)

from cdk_pug_platform.models.monitoring.trackable_service import TrackableService
from cdk_pug_platform.models.monitoring.drawable_service import DrawableService
from cdk_pug_platform.models.tenants.tenant_base import TenantBase

TITLE_HEIGHT = 2


class ApplicationDashboard(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        database_instances: list[Enum],
        drawable_services: list[DrawableService],
        trackable_wit_alarm_services: list[TrackableService],
        database_instance_is_unique: bool = False,
        **kwargs,
    ):
        super().__init__(scope, "app-dashboard", **kwargs)

        APPLICATION_DASHBOARD_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-dashboard"
        )

        self.widgets: list[list[cloudwatch.IWidget]] = []

        left_widgets = []

        for drawable_service in drawable_services:
            drawable_service_name = (
                str(drawable_service.service_type.value)
                .replace("_", " ")
                .title()
                .replace("-", " ")
                .title()
                .replace(" ", "")
                .title()
            )
            drawing_nickname = f"{drawable_service_name} " f" Metrics"

            modified_metrics = []
            for metric in drawable_service.metrics:
                label = f"{metric.metric_name} [{metric.namespace}]"
                modified_metric = metric.with_(label=label)

                modified_metrics.append(modified_metric)

            left_widgets.append(
                cloudwatch.GraphWidget(
                    legend_position=cloudwatch.LegendPosition.BOTTOM,
                    view=cloudwatch.GraphWidgetView.TIME_SERIES,
                    live_data=True,
                    title=drawing_nickname,
                    left=modified_metrics,
                    left_y_axis=cloudwatch.YAxisProps(min=0, show_units=True),
                    right_y_axis=cloudwatch.YAxisProps(min=0, show_units=True),
                    width=12,
                    height=8,
                )
            )

        self.widgets.append(left_widgets)

        log_group_names = [
            ds.log_group.log_group_name
            for ds in drawable_services
            if ds.log_group is not None
        ]

        db_log_error_names = (
            [
                f"/aws/rds/instance/{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-db-server/error"
            ]
            if database_instance_is_unique
            else [
                f"/aws/rds/instance/{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-{db_instance.value}-db-server/error"
                for db_instance in database_instances
            ]
        )

        log_group_names.extend(db_log_error_names)

        db_instance_names = [db_instance.value for db_instance in database_instances]
        service_names = [service.service_type.value for service in drawable_services]
        service_names = [
            str(name)
            .replace("_", " ")
            .title()
            .replace("-", " ")
            .title()
            .replace(" ", "")
            .title()
            for name in service_names
            if name not in db_instance_names
        ]

        title = f"Last Logs for Services: {' / '.join(service_names)} and DB Instances: {' / '.join(db_instance_names)}"

        logs_widget = cloudwatch.LogQueryWidget(
            log_group_names=log_group_names,
            query_string="fields @timestamp, @message | sort @timestamp desc",
            title=title,
            width=12,
            height=12,
        )

        alarm_status_widget = cloudwatch.AlarmStatusWidget(
            title="All Alarms",
            alarms=[ts.alarm for ts in trackable_wit_alarm_services],
            width=12,
            height=12,
        )

        right_widgets = [logs_widget, alarm_status_widget]
        self.widgets.append(right_widgets)

        self.cw_dashboard = cloudwatch.Dashboard(
            self,
            APPLICATION_DASHBOARD_NAME,
            dashboard_name=APPLICATION_DASHBOARD_NAME,
            widgets=self.widgets,
        )

        cloudwatch_dashboard_url = (
            f"https://{Aws.REGION}.console.aws.amazon.com/"
            f"cloudwatch/home?region={Aws.REGION}"
            f"#dashboards:name={APPLICATION_DASHBOARD_NAME}"
        )
        CfnOutput(
            self,
            "dashboard-output",
            value=cloudwatch_dashboard_url,
            description="CloudWatch Dashboard URL",
            export_name=(f"DashboardURL-{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"),
        )
