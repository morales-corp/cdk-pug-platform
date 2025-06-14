from enum import Enum

DEFAULT_IOPS_THRESHOLD = 3000


class AlarmIopsThresholds(Enum):
    DANGER = int(DEFAULT_IOPS_THRESHOLD * 0.7)
    WARNING = int(DEFAULT_IOPS_THRESHOLD * 0.5)

    @classmethod
    def set_threshold(cls, max_iops: int) -> None:
        cls.DANGER._value_ = int(max_iops * 0.7)
        cls.WARNING._value_ = int(max_iops * 0.5)
