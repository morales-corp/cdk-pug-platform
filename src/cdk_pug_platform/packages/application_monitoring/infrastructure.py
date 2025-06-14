from constructs import Construct
from aws_cdk import (
    Aws,
    aws_sns as sns,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
    aws_sns_subscriptions as sns_subscriptions,
)

from cdk_pug_platform.models.tenants.cross_platform import CrossPlatform, MsTeamsSecrets
from cdk_pug_platform.packages.secrets.parsers import parse_secrets_from_env
from cdk_pug_platform.models.monitoring.trackable_service import TrackableService
from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class ApplicationMonitoring(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        trackable_services: list[TrackableService],
        **kwargs,
    ):
        super().__init__(scope, "app-monitoring", **kwargs)
        self.sns_topic = self.create_sns_topic(tenant)
        self.trackable_wit_alarm_services: list[TrackableService] = []

        for trackable_service in trackable_services:

            self.create_cloudwatch_alarm(tenant, trackable_service)

        self.create_notification_lambda(tenant)

    def create_cloudwatch_alarm(
        self,
        tenant: TenantBase,
        trackable_service: TrackableService,
        evaluation_periods: int = 1,
        missing_data_treatment: cloudwatch.TreatMissingData = (
            cloudwatch.TreatMissingData.MISSING
        ),
    ):
        ALARM_NAME = (
            f"{tenant.COMPANY}-{trackable_service.threshold.name.lower()}-"
            f"{tenant.ENVIRONMENT.value}-"
            f"{trackable_service.service_type.value}-"
            f"{trackable_service.metric.metric_name}-alarm"
        )

        ALARM_DESCRIPTION = (
            f"{trackable_service.metric.metric_name} "
            f"{trackable_service.comparison_operator.value} "
            f"{trackable_service.threshold.value}"
        )

        alarm = cloudwatch.Alarm(
            self,
            ALARM_NAME,
            metric=trackable_service.metric,
            threshold=trackable_service.threshold.value,
            evaluation_periods=evaluation_periods,
            alarm_description=ALARM_DESCRIPTION,
            alarm_name=ALARM_NAME,
            comparison_operator=trackable_service.comparison_operator,
            treat_missing_data=missing_data_treatment,
        )

        sns_action = cloudwatch_actions.SnsAction(self.sns_topic)  # type: ignore
        alarm.add_alarm_action(sns_action)  # type: ignore
        trackable_service.set_alarm(alarm)
        self.trackable_wit_alarm_services.append(trackable_service)

    def create_sns_topic(self, tenant: TenantBase):
        topic_name = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-topic"
        return sns.Topic(self, topic_name, display_name=topic_name)

    def create_notification_lambda(self, tenant: TenantBase):

        MS_TEAMS_SECRET_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-"
            f"{CrossPlatform.MS_TEAMS.value}-secret"
        )

        ms_teams_secret = secretsmanager.Secret(
            self,
            MS_TEAMS_SECRET_NAME,
            description="Microsoft Teams Secret",
            secret_name=MS_TEAMS_SECRET_NAME,
            secret_object_value=parse_secrets_from_env(
                tenant, CrossPlatform.MS_TEAMS, MsTeamsSecrets
            ),
        )

        ms_teams_notifier_lambda = lambda_.Function(
            self,
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-{CrossPlatform.MS_TEAMS.value}-notifier",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=lambda_.Code.from_asset(
                f"src/services/apps/{CrossPlatform.MS_TEAMS.value}-notifier"
            ),
            environment={
                "SECRET_NAME": ms_teams_secret.secret_name,
                "SECRET_REGION": Aws.REGION,
                "TENANT_NAME": tenant.COMPANY,
                "ENVIRONMENT": tenant.ENVIRONMENT.value,
            },
        )

        ms_teams_secret.grant_read(ms_teams_notifier_lambda)

        self.sns_topic.add_subscription(sns_subscriptions.LambdaSubscription(ms_teams_notifier_lambda))  # type: ignore
