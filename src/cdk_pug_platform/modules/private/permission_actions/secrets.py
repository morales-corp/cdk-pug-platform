from cdk_pug_platform.models.modules.permission_action import PermissionAction


class GetSecretPermissionAction(PermissionAction):
    def __init__(self) -> None:
        actions = ["secretsmanager:GetSecretValue"]
        super().__init__(actions)


class UpdateSecretPermissionAction(PermissionAction):
    def __init__(self) -> None:
        actions = [
            "secretsmanager:UpdateSecret",
            "secretsmanager:UpdateSecretVersionStage",
        ]
        super().__init__(actions)
