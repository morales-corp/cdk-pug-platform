from enum import Enum
from abc import ABC
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk.aws_cloudwatch import ComparisonOperator


class TrackableService(ABC):
    def __init__(
        self,
        service_type: Enum,
        metric: cloudwatch.Metric,
        threshold: Enum,
        comparison_operator: ComparisonOperator = (
            ComparisonOperator.GREATER_THAN_THRESHOLD
        ),
    ):
        self.service_type = service_type
        self.metric = metric
        self.threshold = threshold
        self.comparison_operator = comparison_operator

    def set_alarm(self, alarm: cloudwatch.Alarm) -> None:
        self.alarm = alarm
