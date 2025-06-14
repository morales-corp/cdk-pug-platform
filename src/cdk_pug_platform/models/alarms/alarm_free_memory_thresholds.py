import aws_cdk as core
from enum import Enum


class AlarmFreeMemoryThresholds(Enum):
    DANGER = core.Size.gibibytes(1).to_bytes()
    WARNING = core.Size.gibibytes(1.5).to_bytes()
