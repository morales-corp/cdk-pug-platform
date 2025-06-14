import os
import aws_cdk.aws_rds as rds
from cdk_pug_platform.utils.validators.environment_validator import (
    EnvironmentValidator,
    load_dotenv,
)


class PathConfig:
    _REPO_ROOT = os.getcwd()

    _DOT_ENV_FOLDER_ENVIRONMENT_CONFIG_RELATIVE_PATH = "server/aws/cdk/.config"
    _DOT_ENV_MAIN_CONFIG_RELATIVE_PATH = "server/aws/cdk/.env"

    @classmethod
    def get_repo_root(cls) -> str:
        print(f"\033[1;36m✨ Repository Root: \033[1;33m{cls._REPO_ROOT}\033[0m")
        return cls._REPO_ROOT

    @classmethod
    def get_central_dot_env_path(cls) -> str:
        path = os.path.join(cls._REPO_ROOT, cls._DOT_ENV_MAIN_CONFIG_RELATIVE_PATH)
        EnvironmentValidator.validate(path)
        return path

    @classmethod
    def get_folder_environment_config_path(cls) -> str:
        path = os.path.join(
            cls._REPO_ROOT, cls._DOT_ENV_FOLDER_ENVIRONMENT_CONFIG_RELATIVE_PATH
        )
        EnvironmentValidator.validate(path)
        return path


class DeploymentConfig:
    @staticmethod
    def is_first_deployment() -> bool:
        load_dotenv(PathConfig.get_central_dot_env_path())
        is_first_deployment = (
            os.getenv("IS_FIRST_DEPLOYMENT", "false").lower() == "true"
        )
        print(
            f"\033[1;36m✨ Is First Deployment: \033[1;33m{is_first_deployment}\033[0m"
        )
        return is_first_deployment


class SqlServerDatabaseConfig:
    """
    Mayor impact to cost IOPS and throughput.
    The difference between web and express is the cost of the license. aprox: 20$ month
    16000 IOPS, 40 GB storage, 1000 MBps throughput: cost 711.00 USD/month
    16000 IOPS, 40 GB storage, 250 MBps throughput: cost 645.00 USD/month
    10000 IOPS, 40 GB storage, 1000 MBps throughput: cost 579.00 USD/month
    10000 IOPS, 40 GB storage, 250 MBps throughput: cost 513.00 USD/month
    5000 IOPS, 40 GB storage, 250 MBps throughput: cost 403.00 USD/month
    """

    MSSQL_PORT = 1433

    @staticmethod
    def get_sql_express() -> rds.IEngine:
        return rds.DatabaseInstanceEngine.sql_server_ex(
            version=rds.SqlServerEngineVersion.VER_16_00_4095_4_V1
        )

    @staticmethod
    def get_sql_web() -> rds.IEngine:
        return rds.DatabaseInstanceEngine.sql_server_web(
            version=rds.SqlServerEngineVersion.VER_16_00_4095_4_V1
        )
