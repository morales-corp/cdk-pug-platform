from aws_cdk import Stack, Tags

from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class TagRulesBuilder:
    @staticmethod
    def _build_tag_rules(
            stack: Stack,
            tenant: TenantBase):
        required_tags = {
            'company': tenant.COMPANY,
            'product': tenant.PRODUCT.value,
            'environment': tenant.ENVIRONMENT.value
        }

        for key, value in required_tags.items():
            Tags.of(stack).add(key, value)
