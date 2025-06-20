#!/usr/bin/env python3

# Example CDK App for Morales Corp Tenant
# -*- coding: utf-8 -*-

"""
Example CDK App for Morales Corp Tenant
This script sets up the AWS CDK application for the Morales Corp tenant.
"""

from aws_cdk import App, Environment
from server.aws.cdk.tenants.morales_corp import TenantMoralesCorp
from server.aws.cdk.stacks.playground_stack import PlaygroundStack


app = App()

# region tenants
tenant_morales_corp = TenantMoralesCorp()
# endregion

# region tenant-stacks
tenant_morales_corp_playground_stack = PlaygroundStack(
    app,
    tenant_morales_corp.live(),
    env=Environment(
        account=tenant_morales_corp.AWS_ACCOUNT, region=tenant_morales_corp.AWS_REGION
    ),
)
# endregion

app.synth()
