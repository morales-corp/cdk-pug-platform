# region: primitives
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion


# region: origen cdk-pug-platform
from cdk_pug_platform.models.environments.app_environment import AppEnvironment

# endregion


class BaseCoreStack(Stack):
    """CoreStack
    This stack is responsible for creating the core resources for the environments of the tenants/products.
    This resources are not related to the tenant/product itself, but to the environment where the tenant is running.
    Definitions:
    - Base: This stack is the base for the core resources.
    - Core Resources: Applications/Systems that manage, monitor, and control the all shared/tenants resources.
    """

    def __init__(self, scope: Construct, environment: AppEnvironment, **kwargs):
        stack_id = f"core-{environment.value}"
        super().__init__(scope, stack_id, **kwargs)
