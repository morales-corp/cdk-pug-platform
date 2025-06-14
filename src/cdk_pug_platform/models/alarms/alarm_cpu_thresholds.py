from enum import Enum

DEFAULT_CPU_WARNING_THRESHOLD = 25


class AlarmCpuThresholds(Enum):
    DANGER = 50
    WARNING = DEFAULT_CPU_WARNING_THRESHOLD

    @staticmethod
    def set_warning_threshold(threshold: int) -> "Enum":
        class NewAlarmCpuThresholds(Enum):
            WARNING = threshold

        return NewAlarmCpuThresholds.WARNING
