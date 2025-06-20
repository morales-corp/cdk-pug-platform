from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class TenantMoralesCorp(TenantBase):
    """
    Morales Corp tenant configuration.
    """

    def __init__(self):
        super().__init__(
            company="Morales Corp",
            product="Morales Platform",
            aws_account="123456789012",
            aws_region="us-west-2",
            principal_dns="moralescorp.xyz",
            certificate_arn="arn:aws:acm:us-west-2:123456789012:certificate/abcd1234-5678-90ab-cdef-EXAMPLE11111",
            prefix_list_cidrs=[
                "192.168.1.1/24",
            ]
        )

    def live(self):
        super().live()

    def uat(self):
        super().uat()

    def dev(self):
        super().dev()
