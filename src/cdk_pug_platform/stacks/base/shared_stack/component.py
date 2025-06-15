# region: primitives
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.environments.app_environment import AppEnvironment

# endregion


class BaseSharedStack(Stack):
    """SharedStack
    This stack is responsible for creating the  shared resources for the environments of the tenants/products.
    This resources are not related to the tenant/product itself, but to the environment where the tenant is running.
    Definitions:
    - Base: This stack is the base for the shared resources.
    - Shared resources: Applications/Systems that englobe a behavior that is independent of the tenant/product.
    """

    def __init__(self, scope: Construct, environment: AppEnvironment, **kwargs):
        stack_id = f"shared-{environment.value}"
        super().__init__(scope, stack_id, **kwargs)
