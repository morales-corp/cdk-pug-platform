from abc import ABC
from typing import TypeVar, Generic

T = TypeVar("T")


class PugModule(ABC, Generic[T]):
    _service: T

    def __init__(self, service: T):
        if service is None:
            raise ValueError("Service is not initialized")

        self._service = service

    def play(self) -> T:
        return self._service
