# region: primitives
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: origen cdk-pug-platform
from cdk_pug_platform.build.tag_rules_builder import TagRulesBuilder
# endregion

from tenants.origen_corp.tenant_origen_corp import TenantOrigenCorp


class PlaygroundStack(
    Stack,
    TagRulesBuilder
):
    def __init__(
            self,
            scope: Construct,
            tenant: TenantOrigenCorp,
            **kwargs
    ):
        stack_id = f"playground-{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"

        super().__init__(scope, stack_id, **kwargs)
