#!/usr/bin/env python3

from cdk_pug_platform.stacks.one_time_ec2_config_stack.component import OneTimeEc2ConfigStack
from stacks.tenant_stack.component import TenantStack
from stacks.playground_stack.component import PlaygroundStack
from aws_cdk import App, Environment


app = App()

# region tenants
tenant_morales_corp = TenantmoralesCorp()
# endregion

# region one-time-ec2-config-stacks
one_time_ec2_config_morales_corp_stack = OneTimeEc2ConfigStack(
    app,
    tenant_morales_corp,
    env=Environment(
        account=tenant_morales_corp.AWS_ACCOUNT, region=tenant_morales_corp.AWS_REGION
    ),
)
# endregion

# region tenant-stacks
tenant_morales_corp_dev_stack = TenantStack(
    app,
    tenant_morales_corp.live(),
    env=Environment(
        account=tenant_morales_corp.AWS_ACCOUNT, region=tenant_morales_corp.AWS_REGION
    ),
)

tenant_morales_corp_playground_stack = PlaygroundStack(
    app,
    tenant_morales_corp.live(),
    env=Environment(
        account=tenant_morales_corp.AWS_ACCOUNT, region=tenant_morales_corp.AWS_REGION
    ),
)
# endregion

app.synth()
