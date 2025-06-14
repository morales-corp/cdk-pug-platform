import aws_cdk as core
from enum import Enum


class AlarmFreeStorageThresholds(Enum):
    DANGER = core.Size.gibibytes(1).to_bytes()
    WARNING = core.Size.gibibytes(5).to_bytes()
