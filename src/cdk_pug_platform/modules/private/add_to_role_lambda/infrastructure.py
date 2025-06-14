from typing import Sequence
from aws_cdk import aws_lambda as _lambda, aws_iam as iam

from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.modules.permission_action import PermissionAction
from cdk_pug_platform.models.modules.runtime.runtime_function import RuntimeIFunction


class AddToRoleLambdaParams:
    objective: str
    lambda_function: _lambda.IFunction
    _permission_actions: Sequence[PermissionAction]
    arn_resources: list[str]

    def __init__(
        self,
        objective: str,
        lambda_function: _lambda.IFunction,
        permission_actions: Sequence[PermissionAction],
        arn_resources: list[str],
    ) -> None:
        self.objective = objective
        self._validate_objective()
        self.lambda_function = lambda_function
        self._permission_actions = permission_actions
        self.arn_resources = arn_resources

    @property
    def all_actions(self) -> list[str]:
        return [
            action
            for permission_action in self._permission_actions
            for action in permission_action.actions
        ]

    def _validate_objective(self) -> None:
        # not should contain any special characters more than -
        assert self.objective.replace("-", "").isalnum()
        # not should contain any spaces
        assert " " not in self.objective
        # not should contain any uppercase characters
        assert self.objective.islower()


class AddToRoleLambdaPug(PugModule[_lambda.IFunction]):
    def __init__(self, params: AddToRoleLambdaParams):
        params.lambda_function.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=params.all_actions, resources=params.arn_resources
            )
        )

        assert isinstance(params.lambda_function, RuntimeIFunction)

        super().__init__(params.lambda_function)
