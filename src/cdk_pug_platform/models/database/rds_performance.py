from aws_cdk.aws_rds import IEngine
from cdk_pug_platform.models.database.engine_types import EngineTypes
from cdk_pug_platform.models.database.instance_family import InstanceFamily
from cdk_pug_platform.models.database.instance_size import InstanceSize


class RdsPerformance:
    VALID_CONFIGURATIONS = {
        EngineTypes.AURORA: [
            InstanceFamily.T3,
            InstanceFamily.T4G,
            InstanceFamily.R6G,
            InstanceFamily.R5,
        ],
        EngineTypes.AURORA_POSTGRESQL: [
            InstanceFamily.T3,
            InstanceFamily.T4G,
            InstanceFamily.R6G,
            InstanceFamily.R5,
        ],
        EngineTypes.MYSQL: [
            InstanceFamily.T2,
            InstanceFamily.T3,
            InstanceFamily.M5,
            InstanceFamily.M6G,
        ],
        EngineTypes.POSTGRESQL: [
            InstanceFamily.T3,
            InstanceFamily.M5,
            InstanceFamily.M6G,
            InstanceFamily.R5,
        ],
        EngineTypes.MARIADB: [InstanceFamily.T3, InstanceFamily.M5, InstanceFamily.R5],
        EngineTypes.ORACLE_EE: [
            InstanceFamily.M5,
            InstanceFamily.R5,
            InstanceFamily.X1E,
        ],
        EngineTypes.SQLSERVER_EE: [
            InstanceFamily.M5,
            InstanceFamily.R5,
            InstanceFamily.X1E,
        ],
        EngineTypes.SQLSERVER_SE: [
            InstanceFamily.T3,
            InstanceFamily.M5,
            InstanceFamily.R5,
        ],
        EngineTypes.SQLSERVER_WEB: [InstanceFamily.T3, InstanceFamily.M5],
        EngineTypes.SQLSERVER_EX: [InstanceFamily.T3],
    }

    def __init__(
        self,
        engine: IEngine,
        instance_family: InstanceFamily,
        instance_size: InstanceSize,
    ):
        self.engine = engine
        self.engine_type = EngineTypes(self.engine.engine_type)
        self.instance_family = instance_family
        self.instance_size = instance_size
        self.instance_type = f"{self.instance_family.value}{self.instance_size.value}"

        self.validate_configuration()

    def validate_configuration(self):
        valid_families = self.VALID_CONFIGURATIONS.get(self.engine_type, [])
        if self.instance_family not in valid_families:
            raise ValueError(
                f"The instance family {self.instance_family.value} "
                f"is not valid for the engine type "
                f"{self.engine_type.value}."
            )
