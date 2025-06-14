from abc import ABC
from enum import Enum
from typing import Optional, List
from aws_cdk import aws_cloudwatch as cloudwatch, aws_logs as logs


class DrawableService(ABC):
    def __init__(
        self,
        service_type: Enum,
        metrics: List[cloudwatch.Metric],
        log_group: Optional[logs.LogGroup] = None,
    ):
        self.service_type = service_type
        self.metrics = metrics
        self.log_group = log_group
