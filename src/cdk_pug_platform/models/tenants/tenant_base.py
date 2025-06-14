from enum import Enum
from typing import Optional
from cdk_pug_platform.models.environments.app_environment import AppEnvironment
from cdk_pug_platform.models.blueprints.ecs_fargate_blueprint import EcsFargateBlueprint
from cdk_pug_platform.models.blueprints.database_blueprint import DatabaseBlueprint


class IpPrivateRanges(Enum):
    """
    Range of private IP addresses defined by RFC 1918
        • 10.0.0.0/16 - 65536 IP addresses
        • 172.16.0.0/20 - 4096 IP addresses
        • 192.168.0.0/24 - 256 IP addresses
    """

    LARGE_COMPANY = "10"
    BIG_COMPANY = "172.16"
    SMALL_COMPANY = "192.168"


class InfrastructureTypes(Enum):
    ECS_FARGATE_RDS = "ecs_fargate_rds"
    ECS_EC2_RDS = "ecs_ec2_rds"
    RDS_ONLY = "rds_only"


class PrefixListCidr:
    def __init__(
        self,
        cidr: str,
        description: str,
    ):
        self.CIDR = cidr
        self.DESCRIPTION = description

    def validate_cidr(self):
        if "/16" in self.CIDR:
            raise ValueError("CIDR must not be /16")


class TenantBase:
    def __init__(
        self,
        company: str,
        product: Enum,
        aws_account: str,
        aws_region: str,
        principal_dns: str,
        certificate_arn: str,
        ip_private_ranges: IpPrivateRanges,
        infrastructure_type: InfrastructureTypes,
        prefix_list_cidrs: list[PrefixListCidr],
    ):
        self._PRINCIPAL_DNS = principal_dns
        self.COMPANY = company
        self.PRODUCT = product
        self.AWS_ACCOUNT = aws_account
        self.AWS_REGION = aws_region
        self.FEDERATED_DNS = f"{self.PRODUCT.value}.{self._PRINCIPAL_DNS}"
        self.PRIVATE_DNS = f"internal.{self.FEDERATED_DNS}"
        self.CERTIFICATE_ARN = certificate_arn
        self.IP_PRIVATE_RANGES = ip_private_ranges
        self._infrastructure_type = infrastructure_type
        self.PREFIX_LIST_CIDRS = prefix_list_cidrs

    def _builder_blueprints(
        self,
        ecs_fargate_blueprints: Optional[dict[Enum, EcsFargateBlueprint]] = None,
        rds_blueprints: Optional[dict[Enum, DatabaseBlueprint]] = None,
    ):
        if self._infrastructure_type == InfrastructureTypes.ECS_FARGATE_RDS:
            self._ECS_FARGATE_BLUEPRINTS = ecs_fargate_blueprints
            self._RDS_BLUEPRINTS = rds_blueprints
        elif self._infrastructure_type == InfrastructureTypes.ECS_EC2_RDS:
            raise NotImplementedError(
                f"{InfrastructureTypes.ECS_EC2_RDS.value} " "is not implemented yet"
            )
        elif self._infrastructure_type == InfrastructureTypes.RDS_ONLY:
            self._RDS_BLUEPRINTS = rds_blueprints

    @property
    def ecs_fargate_blueprints(self):
        if self._ECS_FARGATE_BLUEPRINTS is None:
            raise ValueError("ECS Fargate blueprints are not defined for this tenant")
        return self._ECS_FARGATE_BLUEPRINTS

    @property
    def rds_blueprints(self):
        if self._RDS_BLUEPRINTS is None:
            raise ValueError("RDS blueprints are not defined for this tenant")
        return self._RDS_BLUEPRINTS

    def dev(self):
        if self.IP_PRIVATE_RANGES == IpPrivateRanges.LARGE_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".2.0.0/16"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.BIG_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".32.0/20"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.SMALL_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".32.0/24"

        self.ENVIRONMENT = AppEnvironment.DEV

        return self

    def uat(self):
        if self.IP_PRIVATE_RANGES == IpPrivateRanges.LARGE_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".1.0.0/16"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.BIG_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".16.0/20"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.SMALL_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".16.0/24"

        self.ENVIRONMENT = AppEnvironment.UAT

        return self

    def live(self):
        if self.IP_PRIVATE_RANGES == IpPrivateRanges.LARGE_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".0.0.0/16"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.BIG_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".0.0/20"
        elif self.IP_PRIVATE_RANGES == IpPrivateRanges.SMALL_COMPANY:
            self.VPC_CIDR = self.IP_PRIVATE_RANGES.value + ".0.0/24"

        self.ENVIRONMENT = AppEnvironment.LIVE

        return self
