from enum import Enum


class DatabasePrivileges(Enum):
    READ_ONLY = "r"
    READ_WRITE = "rw"
    ADMIN = "admin"
