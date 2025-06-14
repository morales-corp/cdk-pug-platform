from enum import Enum


class EngineTypes(Enum):
    AURORA = "aurora"
    AURORA_POSTGRESQL = "aurora-postgresql"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MARIADB = "mariadb"
    ORACLE_EE = "oracle-ee"
    ORACLE_SE2 = "oracle-se2"
    ORACLE_SE1 = "oracle-se1"
    ORACLE_SE = "oracle-se"
    SQLSERVER_EE = "sqlserver-ee"
    SQLSERVER_SE = "sqlserver-se"
    SQLSERVER_EX = "sqlserver-ex"
    SQLSERVER_WEB = "sqlserver-web"
