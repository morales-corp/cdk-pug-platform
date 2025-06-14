from enum import Enum
from constants import (
    COMPANY,
    AWS_DEFAULT_ACCOUNT,
    AWS_DEFAULT_REGION,
    PRODUCT,
    ORIGEN_CORP_CIDR,
    IAC_LEAD_HOME_CIDR
)
from cdk_pug_platform.models.environments.app_environment import AppEnvironment
from cdk_pug_platform.models.tenants.tenant_base import (
    InfrastructureTypes,
    IpPrivateRanges,
    PrefixListCidr,
    TenantBase
)


class Products(Enum):
    ORIGEN_IAC = PRODUCT


class TenantOrigenCorp(TenantBase):
    def __init__(
        self,
    ):
        super().__init__(
            company=COMPANY,
            product=Products.ORIGEN_IAC,
            aws_account=AWS_DEFAULT_ACCOUNT,
            aws_region=AWS_DEFAULT_REGION,
            principal_dns="research.life.origen.bio",
            certificate_arn="arn:aws:acm:eu-west-3:111856684272:certificate/0cf220a1-0745-4f63-996f-08543b6b2108",
            ip_private_ranges=IpPrivateRanges.LARGE_COMPANY,
            infrastructure_type=InfrastructureTypes.ECS_FARGATE_RDS,
            prefix_list_cidrs=[
                PrefixListCidr(
                    cidr=ORIGEN_CORP_CIDR,
                    description="Origen Office Corp CIDR"
                ),
                PrefixListCidr(
                    cidr=IAC_LEAD_HOME_CIDR,
                    description="IAC Lead Home CIDR"
                )
            ]
        )

    def live(self):
        super().live()

        self.ENVIRONMENT = AppEnvironment.LIVE

        return self
