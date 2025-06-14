from typing import runtime_checkable, Protocol

from aws_cdk import (
    aws_lambda as lambda_,
)


@runtime_checkable
class RuntimeIEventSource(lambda_.IEventSource, Protocol):
    pass
