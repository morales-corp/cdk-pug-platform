from enum import Enum

DEFAULT_MEMORY_WARNING_THRESHOLD = 25


class AlarmMemoryThresholds(Enum):
    DANGER = 50
    WARNING = DEFAULT_MEMORY_WARNING_THRESHOLD

    @staticmethod
    def set_warning_threshold(threshold: int) -> "Enum":
        class NewAlarmMemoryThresholds(Enum):
            WARNING = threshold

        return NewAlarmMemoryThresholds.WARNING
