from pydantic import BaseModel, Field, model_validator, ConfigDict

from cdk_pug_platform.models.alarms import AlarmCpuThresholds, AlarmMemoryThresholds

DEFAULT_MIN_CAPACITY = 1
DEFAULT_MAX_CAPACITY = 30

LOWER_GRADIENT = 20
UPPER_GRADIENT = 10

trigger_percent_cpu_default = AlarmCpuThresholds.WARNING.value
trigger_percent_memory_default = AlarmMemoryThresholds.WARNING.value


class ScalingRule(BaseModel):
    model_config = ConfigDict(validate_default=True, extra="forbid")

    min_capacity: int = Field(
        default=DEFAULT_MIN_CAPACITY,
        ge=DEFAULT_MIN_CAPACITY,
        le=DEFAULT_MAX_CAPACITY,
        description="Minimum number of instances to keep running",
    )

    max_capacity: int = Field(
        default=DEFAULT_MIN_CAPACITY,
        ge=DEFAULT_MIN_CAPACITY,
        le=DEFAULT_MAX_CAPACITY,
        description="Maximum number of instances to keep running",
    )

    trigger_percent_cpu: int = Field(
        default=trigger_percent_cpu_default,
        ge=trigger_percent_cpu_default - LOWER_GRADIENT,
        le=trigger_percent_cpu_default + UPPER_GRADIENT,
        description="Target CPU usage to trigger scaling",
    )

    trigger_percent_memory: int = Field(
        default=trigger_percent_memory_default,
        ge=trigger_percent_memory_default - LOWER_GRADIENT,
        le=trigger_percent_memory_default + UPPER_GRADIENT,
        description="Target memory usage to trigger scaling",
    )

    @model_validator(mode="after")
    def validate_capacity(cls, values) -> "ScalingRule":
        if values.min_capacity > values.max_capacity:
            raise ValueError("min_capacity must be less than or equal to max_capacity")
        return values

    @model_validator(mode="after")
    def validate_trigger_percent(cls, values) -> "ScalingRule":

        if values.trigger_percent_cpu > 80:
            raise ValueError("trigger_percent_cpu must be less than 80")

        if values.trigger_percent_memory > 80:
            raise ValueError("trigger_percent_memory must be less than 80")

        return values
