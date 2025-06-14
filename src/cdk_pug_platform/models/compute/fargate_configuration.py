from typing import List
from enum import Enum
from cdk_pug_platform.models.compute.operating_system import OperatingSystem


class FargateVirtualCpu(Enum):
    VCPU_0_25 = 256
    VCPU_0_5 = 512
    VCPU_1 = 1024
    VCPU_2 = 2048
    VCPU_4 = 4096
    VCPU_8 = 8192
    VCPU_16 = 16384


class FargateConfiguration:
    def __init__(
        self,
        cpu: int,
        memory_limits: List[int],
        operating_systems: List[OperatingSystem],
    ):
        """
        :param cpu: CPU value in vCPU.
        :param memory_limits: List of allowed memory values (in MiB).
        :param operating_systems: List of supported operating systems.
        """
        self.cpu = cpu
        self.memory_limits = memory_limits
        self.operating_systems = operating_systems

    def validate_memory(self, memory: int):
        """Validate if the memory is within allowed limits."""
        if memory not in self.memory_limits:
            raise ValueError(
                f"Memory value {memory} MiB is not valid for CPU {self.cpu}. "
                f"Allowed values: {self.memory_limits}"
            )


# consult the documentation for the correct values: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html # noqa
class FargateConfigurations:
    CONFIGURATIONS = {
        FargateVirtualCpu.VCPU_0_25: FargateConfiguration(
            FargateVirtualCpu.VCPU_0_25.value,
            [512, 1024, 2048],
            [OperatingSystem.LINUX],
        ),
        FargateVirtualCpu.VCPU_0_5: FargateConfiguration(
            FargateVirtualCpu.VCPU_0_5.value,
            [1024, 2048, 3072, 4096],
            [OperatingSystem.LINUX],
        ),
        FargateVirtualCpu.VCPU_1: FargateConfiguration(
            FargateVirtualCpu.VCPU_1.value,
            [2048, 3072, 4096, 5120, 6144, 7168, 8192],
            [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
        ),
        FargateVirtualCpu.VCPU_2: FargateConfiguration(
            FargateVirtualCpu.VCPU_2.value,
            list(range(4096, 16385, 1024)),
            [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
        ),
        FargateVirtualCpu.VCPU_4: FargateConfiguration(
            FargateVirtualCpu.VCPU_4.value,
            list(range(8192, 30721, 1024)),
            [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
        ),
        FargateVirtualCpu.VCPU_8: FargateConfiguration(
            FargateVirtualCpu.VCPU_8.value,
            list(range(16384, 61441, 4096)),
            [OperatingSystem.LINUX],
        ),
        FargateVirtualCpu.VCPU_16: FargateConfiguration(
            FargateVirtualCpu.VCPU_16.value,
            list(range(32768, 122881, 8192)),
            [OperatingSystem.LINUX],
        ),
    }

    @classmethod
    def get_by_layer(cls, layer: FargateVirtualCpu) -> FargateConfiguration:
        """Gets configuration by Fargate layer."""
        if layer not in cls.CONFIGURATIONS:
            raise ValueError(f"Configuration for layer {layer} not found.")
        return cls.CONFIGURATIONS[layer]
