from pydantic import BaseModel, Field

from cdk_pug_platform.models.database.database_privileges import DatabasePrivileges


class ServiceUserSecret(BaseModel):
    secret_arn: str = Field(..., description="The ARN of the secret.")
    privilege: DatabasePrivileges = Field(..., description="The privilege of the user.")
    password_is_recreable: bool = Field(
        ..., description="Whether the password is recreable."
    )
