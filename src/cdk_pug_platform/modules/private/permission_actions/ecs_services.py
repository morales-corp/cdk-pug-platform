from cdk_pug_platform.models.modules.permission_action import PermissionAction


class UpdateServicePermissionAction(PermissionAction):
    def __init__(self) -> None:
        actions = ["ecs:UpdateService"]
        super().__init__(actions)
