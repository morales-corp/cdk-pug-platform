from aws_cdk import (
    aws_ec2 as ec2,
)

from constructs import Construct
from cdk_pug_platform.models.tenants.tenant_base import TenantBase


class Networking(Construct):
    def __init__(
        self, scope: Construct, tenant: TenantBase, available_zones: int, **kwargs
    ):
        super().__init__(scope, "networking", **kwargs)

        PREFIX_LIST_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-prefix-list"
        entries = [
            ec2.CfnPrefixList.EntryProperty(
                cidr=prefix_list_cidr.CIDR,
                description=prefix_list_cidr.DESCRIPTION,
            )
            for prefix_list_cidr in tenant.PREFIX_LIST_CIDRS
        ]
        self.prefix_list = ec2.PrefixList(
            self,
            PREFIX_LIST_NAME,
            address_family=ec2.AddressFamily.IP_V4,
            prefix_list_name=PREFIX_LIST_NAME,
            entries=entries,
        )

        TENANT_VPC_NAME = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-vpc"
        self.tenant_vpc = ec2.Vpc(
            self,
            TENANT_VPC_NAME,
            vpc_name=TENANT_VPC_NAME,
            ip_addresses=ec2.IpAddresses.cidr(tenant.VPC_CIDR),  # type: ignore
            nat_gateways=1,
            max_azs=available_zones,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{TENANT_VPC_NAME}-subnet-public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name=f"{TENANT_VPC_NAME}-subnet-private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
                ec2.SubnetConfiguration(
                    name=f"{TENANT_VPC_NAME}-subnet-isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
        )

        self.tenant_vpc.add_flow_log(
            f"{TENANT_VPC_NAME}-flow-log",
            destination=ec2.FlowLogDestination.to_cloud_watch_logs(),
            max_aggregation_interval=ec2.FlowLogMaxAggregationInterval.TEN_MINUTES,
            traffic_type=ec2.FlowLogTrafficType.REJECT,
        )

        self.tenant_vpc.add_interface_endpoint(
            "EfsVpcEndpoint",
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            service=ec2.InterfaceVpcEndpointAwsService.ELASTIC_FILESYSTEM,
        )
