from enum import Enum
from typing import Optional
from cdk_pug_platform.models.database.service_user_secret import ServiceUserSecret
from cdk_pug_platform.models.environments.app_environment import AppEnvironment

type _DatabaseInstances = Enum
type _PersistentDatabases = Enum
type _Services = Enum

_MatrixSeedType = dict[_DatabaseInstances, list[_PersistentDatabases]]
_MatrixEnvironmentSeed = dict[AppEnvironment, _MatrixSeedType]
_VectorServiceSecret = dict[_Services, ServiceUserSecret]
_VectorPersistentServices = dict[_PersistentDatabases, _VectorServiceSecret]
_MatrixType = dict[_DatabaseInstances, _VectorPersistentServices]


class DatabaseMatrix:
    _matrix_seed_by_environment: dict[str, _MatrixSeedType] = None
    _matrix_seed: _MatrixSeedType = {}
    _vector_persistent_services: list[_VectorPersistentServices] = []

    def set_matrix_seed(self, matrix_seed: _MatrixSeedType):
        self._matrix_seed = matrix_seed

        return self

    def set_matrix_seed_by_environment(
        self, matrix_seed_by_environment: _MatrixEnvironmentSeed
    ):
        self._matrix_seed_by_environment = matrix_seed_by_environment

        return self

    def add_vector_persistent_service(self, vector: _VectorPersistentServices):
        self._vector_persistent_services.append(vector)

        return self

    def build(self, environment: Optional[AppEnvironment] = None) -> _MatrixType:
        matrix: _MatrixType = {}

        items = []
        if self._matrix_seed_by_environment and environment:
            items = self._matrix_seed_by_environment[environment].items()
        else:
            items = self._matrix_seed.items()
        for instance, persistents in items:
            matrix[instance] = {}
            for persistent in persistents:
                merged_services: _VectorServiceSecret = {}
                for vector in self._vector_persistent_services:
                    if persistent in vector:
                        merged_services.update(vector[persistent])
                matrix[instance][persistent] = merged_services
        return matrix
