from cdk_pug_platform.models.tenants.tenant_base import TenantBase

from aws_cdk import aws_servicecatalogappregistry as appreg
from constructs import Construct


class ApplicationManager(Construct):
    def __init__(self, scope: Construct, tenant: TenantBase, stack_id: str, **kwargs):
        super().__init__(scope, "application-manager", **kwargs)
        app = appreg.CfnApplication(
            self,
            "app",
            name=f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}",
            description=f"{tenant.COMPANY} {tenant.ENVIRONMENT.value}",
        )

        appreg.CfnResourceAssociation(
            self,
            "app-resource",
            application=app.attr_id,
            resource_type="CFN_STACK",
            resource=stack_id,
        )
