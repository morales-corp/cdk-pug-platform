from typing import Sequence, Optional
from cdk_pug_platform.models.containers.ecs_fargate_types import EcsFargateTypes
from cdk_pug_platform.models.compute.fargate_task_compute import FargateTaskCompute
from cdk_pug_platform.models.compute.compute_time_configuration import (
    ComputeTimeConfiguration,
)
from cdk_pug_platform.models.compute.scaling_rule import ScalingRule


class EcsFargateBlueprint:
    def __init__(
        self,
        ecs_fargate_type: EcsFargateTypes,
        compute: FargateTaskCompute,
        command: Sequence[str],
        entry_point: Sequence[str],
        time_configuration: ComputeTimeConfiguration,
        scaling_rule: Optional[ScalingRule] = None,
        desired_task_count: Optional[int] = None,
        schedule: Optional[str] = None,
    ):
        self.ecs_fargate_type = ecs_fargate_type
        self.compute = compute
        """
        The command to run in the container. The command is the first part of the entry point.
        Depending on the operating system console.
        Example: [
            "/bin/sh",
            "-c"
        ]
        """
        self.command = command
        """
        The entry point for the container. This is the first part of the command.
        Depending on the language code that is being run.
        This entry point overrides the default entry point.
        Example: [
            "dotnet",
            "Project.dll",
        ]
        Example: [
            "python",
            "app.py"
        ]
        """
        self.entry_point = entry_point

        self.time_configuration = time_configuration
        self._scaling_rule = scaling_rule
        self._desired_task_count = desired_task_count
        self._schedule = schedule

        required_fields = {
            EcsFargateTypes.SERVICE: {"scaling_rule": self._scaling_rule},
            EcsFargateTypes.SCHEDULED_TASK: {
                "desired_task_count": self._desired_task_count,
                "schedule": self._schedule,
            },
        }

        if self.ecs_fargate_type in required_fields:
            for field_name, field_value in required_fields[
                self.ecs_fargate_type
            ].items():
                assert (
                    field_value
                ), f"{field_name} is required for ECS Fargate type {self.ecs_fargate_type}"
        else:
            raise ValueError(f"Invalid ECS Fargate type {self.ecs_fargate_type}")

    @property
    def scaling_rule(self) -> ScalingRule:
        assert (
            self._scaling_rule
        ), "scaling_rule is required for ECS Fargate type SERVICE"

        return self._scaling_rule

    @property
    def desired_task_count(self) -> int:
        assert (
            self._desired_task_count
        ), "desired_task_count is required for ECS Fargate type SCHEDULED_TASK"

        return self._desired_task_count

    @property
    def schedule(self) -> str:
        assert (
            self._schedule
        ), "schedule is required for ECS Fargate type SCHEDULED_TASK"

        self._validate_cron_expression()

        return self._schedule

    def _validate_cron_expression(self):
        if not self._schedule or not self._schedule.startswith("cron"):
            raise ValueError("Invalid cron expression")
