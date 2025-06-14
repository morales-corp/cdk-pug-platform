#!/usr/bin/env python3

from tenants.origen_corp.tenant_origen_corp import TenantOrigenCorp
from cdk_pug_platform.stacks.one_time_ec2_config_stack.component import OneTimeEc2ConfigStack
from stacks.tenant_stack.component import TenantStack
from stacks.playground_stack.component import PlaygroundStack
from aws_cdk import App, Environment


app = App()

# region tenants
tenant_origen_corp = TenantOrigenCorp()
# endregion

# region one-time-ec2-config-stacks
one_time_ec2_config_origen_corp_stack = OneTimeEc2ConfigStack(
    app,
    tenant_origen_corp,
    env=Environment(
        account=tenant_origen_corp.AWS_ACCOUNT, region=tenant_origen_corp.AWS_REGION
    ),
)
# endregion

# region tenant-stacks
tenant_origen_corp_dev_stack = TenantStack(
    app,
    tenant_origen_corp.live(),
    env=Environment(
        account=tenant_origen_corp.AWS_ACCOUNT, region=tenant_origen_corp.AWS_REGION
    ),
)

tenant_origen_corp_playground_stack = PlaygroundStack(
    app,
    tenant_origen_corp.live(),
    env=Environment(
        account=tenant_origen_corp.AWS_ACCOUNT, region=tenant_origen_corp.AWS_REGION
    ),
)
# endregion

app.synth()
