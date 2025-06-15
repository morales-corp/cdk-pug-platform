# region: primitives
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.packages.instance_key_pair.infrastructure import (
    InstanceKeyPair,
    OperatingSystem,
)

# endregion


class OneTimeEc2ConfigStack(Stack):
    """OneTimeEc2ConfigStack
    This stack is responsible for creating the EC2 resources for the remote connections for EC2 instances.
    """

    def __init__(self, scope: Construct, **kwargs):
        stack_id = "one-time-ec2-config"

        super().__init__(scope, stack_id, termination_protection=True, **kwargs)

        self.windows_key_pair = InstanceKeyPair(
            self, stack_id, operating_system=OperatingSystem.WINDOWS
        )

        self.linux_key_pair = InstanceKeyPair(
            self, stack_id, operating_system=OperatingSystem.LINUX
        )
