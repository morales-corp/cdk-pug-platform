from jsii import Number
from cdk_pug_platform.models.compute.fargate_configuration import (
    OperatingSystem,
    FargateConfigurations,
)


class FargateTaskCompute:
    def __init__(self, cpu: Number, memory_limit_mib: Number, os: OperatingSystem):
        """
        :param cpu: CPU value in vCPU.
        :param memory_limit_mib: Desired memory in MiB.
        :param os: Desired operating system.
        """
        # Match configuration by CPU
        layer = next(
            (
                layer
                for layer, config in FargateConfigurations.CONFIGURATIONS.items()
                if config.cpu == cpu and os in config.operating_systems
            ),
            None,
        )
        if not layer:
            raise ValueError(f"No configuration found for CPU {cpu} and OS {os}.")

        # Validate memory
        config = FargateConfigurations.CONFIGURATIONS[layer]
        config.validate_memory(int(memory_limit_mib))

        self.cpu = cpu
        self.memory_limit_mib = memory_limit_mib
        self.operating_system = os
