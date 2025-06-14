# region: primitives
from enum import Enum
from constructs import Construct

# endregion

# region: aws-cdk
import aws_cdk as core
from aws_cdk import aws_logs as logs

# endregion

# region origen cdk-pug-platform
from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.tenants.tenant_base import TenantBase

# endregion


class LogGroupPug(PugModule[logs.LogGroup]):
    def __init__(self, scope: Construct, tenant: TenantBase, service_type: Enum):
        LOG_GROUP_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-{service_type.value}-log-group"

        self.log_group = logs.LogGroup(
            scope,
            LOG_GROUP_NAME,
            log_group_name=LOG_GROUP_NAME,
            retention=logs.RetentionDays.ONE_MONTH,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        super().__init__(self.log_group)
