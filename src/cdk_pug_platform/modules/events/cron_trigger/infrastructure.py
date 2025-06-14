from typing import Optional
from constructs import Construct

from aws_cdk import aws_events as events

from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.modules.runtime.runtime_rule_target import (
    RuntimeIRuleTarget,
)
from cdk_pug_platform.models.modules.runtime.runtime_rule import RuntimeIRule
from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class CronTriggerParams:
    target_name: str
    target: events.IRuleTarget
    schedule: str
    description: Optional[str] = None

    def __init__(
        self,
        target_name: str,
        target: events.IRuleTarget,
        schedule: str,
        description: Optional[str] = None,
    ) -> None:
        self.target_name = target_name
        self.target = target
        self.schedule = schedule
        self.validate_cron_expression()
        self.description = description

    def validate_cron_expression(self):
        if not self.schedule.startswith("cron"):
            raise ValueError("Invalid cron expression")


class CronTrigger(PugModule[events.IRule]):
    def __init__(
        self, scope: Construct, tenant: TenantBase, params: CronTriggerParams
    ) -> None:
        TENANT_ENVIRONMENT_TARGET_NAME = (
            f"{tenant.COMPANY}-" f"{tenant.ENVIRONMENT.value}-" f"{params.target_name}"
        )

        rule = events.Rule(
            scope,
            f"{TENANT_ENVIRONMENT_TARGET_NAME}-rule",
            schedule=events.Schedule.expression(params.schedule),
        )

        assert isinstance(params.target, RuntimeIRuleTarget)
        rule.add_target(params.target)

        assert isinstance(rule, RuntimeIRule)
        super().__init__(rule)
