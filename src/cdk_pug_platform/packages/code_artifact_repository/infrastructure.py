from constructs import Construct

from aws_cdk import aws_codeartifact as codeartifact

from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class CodeArtifactRepository(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        domain_name: str,
        repository_name: str,
        repository_description: str,
        **kwargs,
    ):
        super().__init__(scope, "code-artifact-repository", **kwargs)
        REPOSITORY_NAME = (
            f"{tenant.COMPANY}-" f"{tenant.ENVIRONMENT.value}-" f"{repository_name}"
        )

        self.repository = codeartifact.CfnRepository(
            self,
            REPOSITORY_NAME,
            domain_name=domain_name,
            domain_owner=tenant.AWS_ACCOUNT,
            repository_name=repository_name,
            description=repository_description,
        )
