from constructs import Construct

from aws_cdk import aws_codeartifact as codeartifact

from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class CodeArtifactDomain(Construct):
    def __init__(self, scope: Construct, tenant: TenantBase, **kwargs):
        super().__init__(scope, "code-artifact-domain", **kwargs)
        DOMAIN_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"

        self.domain = codeartifact.CfnDomain(self, DOMAIN_NAME, domain_name=DOMAIN_NAME)
