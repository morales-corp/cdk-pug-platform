from typing import runtime_checkable, Protocol

from aws_cdk import aws_events as events


@runtime_checkable
class RuntimeIRuleTarget(events.IRuleTarget, Protocol):
    pass
