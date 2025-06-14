# region: primitives
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: origen cdk-pug-platform
from cdk_pug_platform.packages.networking.infrastructure import Networking
from cdk_pug_platform.build.tag_rules_builder import TagRulesBuilder
from cdk_pug_platform.packages.code_artifact_domain.infrastructure import (
    CodeArtifactDomain,
)
from cdk_pug_platform.packages.code_artifact_repository.infrastructure import (
    CodeArtifactRepository,
)
from cdk_pug_platform.packages.instance_operations.infrastructure import (
    InstanceOperations,
)
# endregion

from tenants.origen_corp.tenant_origen_corp import TenantOrigenCorp

from constants import PRODUCT, PRODUCT_DESCRIPTION


class TenantStack(Stack, TagRulesBuilder):
    def __init__(self, scope: Construct, tenant: TenantOrigenCorp, **kwargs):
        stack_id = f"tenant-{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"

        super().__init__(scope, stack_id, **kwargs)

        self.code_artifact_domain = CodeArtifactDomain(self, tenant)

        self.code_artifact_repository = CodeArtifactRepository(
            self,
            tenant,
            self.code_artifact_domain.domain.domain_name,
            PRODUCT,
            PRODUCT_DESCRIPTION
        )

        self.code_artifact_repository.repository.node.add_dependency(
            self.code_artifact_domain.domain
        )

        self.networking = Networking(
            self,
            tenant,
            available_zones=1
        )
        self.instance_operations = InstanceOperations(
            self,
            tenant,
            self.networking.tenant_vpc,
            self.networking.prefix_list
        )
