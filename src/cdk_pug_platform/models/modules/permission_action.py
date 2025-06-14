class PermissionAction:
    _actions = []

    def __init__(self, actions: list[str]) -> None:
        self._actions = actions

    @property
    def actions(self) -> list[str]:
        return self._actions
