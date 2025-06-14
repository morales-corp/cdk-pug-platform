from enum import Enum


class RegistryTypes(Enum):
    ECR = "ecr"
    PRIVATE = "private"
    PUBLIC = "public"
