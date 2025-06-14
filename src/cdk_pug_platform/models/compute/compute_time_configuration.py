import aws_cdk as core
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional

DEFAULT_TIMEOUT_SECONDS = 60


class ComputeTimeConfiguration(BaseModel):
    model_config = ConfigDict(validate_default=True, extra="forbid")

    # DB_COMMAND_TIMEOUT
    db_command_timeout_seconds: Optional[int] = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        ge=0,
        le=60 * 60,
        description="Timeout for DB commands in seconds",
    )

    db_command_timeout_minutes: Optional[int] = Field(
        default=None, ge=0, le=60, description="Timeout for DB commands in minutes"
    )

    # idle_timeout
    load_balancer_timeout_seconds: Optional[int] = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        ge=60,
        le=4000,
        description="Timeout for load balancer in seconds",
    )

    load_balancer_timeout_minutes: Optional[int] = Field(
        default=None, ge=1, le=60, description="Timeout for load balancer in minutes"
    )

    # health_check interval
    health_check_interval_seconds: Optional[int] = Field(
        default=5, ge=5, le=300, description="Interval between health checks in seconds"
    )
    health_check_interval_minutes: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Interval between health checks in minutes",
    )

    # health_check timeout
    health_check_timeout_seconds: Optional[int] = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        ge=2,
        le=120,
        description="Timeout for health checks in seconds",
    )

    health_check_timeout_minutes: Optional[int] = Field(
        default=None, ge=1, le=2, description="Timeout for health checks in minutes"
    )

    # health path
    health_path: Optional[str] = Field(
        default="/health", description="Health path for health checks"
    )

    # healthy_http_codes
    healthy_http_codes: Optional[str] = Field(
        default="200", description="Healthy HTTP codes for health checks"
    )

    # unhealthy_threshold_count and healthy_threshold_count
    unhealthy_threshold_count: Optional[int] = Field(
        default=2,
        ge=2,
        le=10,
        description="Unhealthy threshold count for health checks",
    )

    healthy_threshold_count: Optional[int] = Field(
        default=2, ge=2, le=10, description="Healthy threshold count for health checks"
    )

    @model_validator(mode="after")
    def convert_minutes_to_seconds(cls, values):
        minutes_to_seconds = [
            ("db_command_timeout_minutes", "db_command_timeout_seconds"),
            ("load_balancer_timeout_minutes", "load_balancer_timeout_seconds"),
            ("health_check_interval_minutes", "health_check_interval_seconds"),
            ("health_check_timeout_minutes", "health_check_timeout_seconds"),
            ("health_check_grace_period_minutes", "health_check_grace_period_seconds"),
        ]
        for minutes_key, seconds_key in minutes_to_seconds:
            minutes = getattr(values, minutes_key, None)
            if minutes is not None:
                setattr(values, seconds_key, minutes * 60)
        return values

    def _get_timeout_duration(self, timeout_seconds: Optional[int], timeout_name: str):
        if timeout_seconds is None:
            raise ValueError(f"{timeout_name} is required")

        return core.Duration.seconds(timeout_seconds)

    @property
    def db_command_timeout(self):
        return self._get_timeout_duration(
            self.db_command_timeout_seconds, "db_command_timeout_seconds"
        )

    @property
    def load_balancer_timeout(self):
        return self._get_timeout_duration(
            self.load_balancer_timeout_seconds, "load_balancer_timeout_seconds"
        )

    @property
    def health_check_interval(self):
        return self._get_timeout_duration(
            self.health_check_interval_seconds, "health_check_interval_seconds"
        )

    @property
    def health_check_timeout(self):
        return self._get_timeout_duration(
            self.health_check_timeout_seconds, "health_check_timeout_seconds"
        )
