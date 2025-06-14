from constructs import Construct

from aws_cdk import (
    aws_ec2 as ec2,
)

from cdk_pug_platform.models.environments.app_environment import AppEnvironment
from cdk_pug_platform.models.compute.operating_system import OperatingSystem
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.models.tenants.cross_platform import CrossPlatform


class PowerBiBastion(Construct):
    """
    Power BI Bastion

    This class defines a Power BI Bastion host within a specified VPC.
    The bastion host is configured to be accessible only from within the VPC
    using AWS Systems Manager (SSM) Session Manager.
    Ensuring it is not exposed to any network outside of the VPC.
    Motivation: The data live environment should not be exposed to the internet.
    !IMPORTANT The risk of use Windows Remote Desktop Protocol (RDP) is high.
    """

    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        tenant_vpc: ec2.Vpc,
        volume_size: int = 45,
        **kwargs,
    ):
        super().__init__(scope, "powerbi-bastion", **kwargs)

        if tenant.ENVIRONMENT == AppEnvironment.LIVE:
            environment_name = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-{CrossPlatform.POWERBI.value}"
            BASTION_SECURITY_GROUP_NAME = f"{environment_name}-bastion-security-group"
            BASTION_NAME = f"{environment_name}-bastion"
            operating_system: OperatingSystem = OperatingSystem.WINDOWS

            self.bastion_security_group = ec2.SecurityGroup(
                self,
                BASTION_SECURITY_GROUP_NAME,
                vpc=tenant_vpc,
                security_group_name=BASTION_SECURITY_GROUP_NAME,
                description="Power BI Bastion Security Group",
                allow_all_outbound=True,
            )

            self.bastion_security_group.add_ingress_rule(
                ec2.Peer.ipv4(tenant_vpc.vpc_cidr_block),
                ec2.Port.tcp(3389),
                "Allow RDP from SSM Session Manager",
            )

            KEY_NAME = f"one-time-ec2-config-{operating_system.value.lower()}-key-pair"

            self.bastion_key = ec2.KeyPair.from_key_pair_name(
                self, KEY_NAME, key_pair_name=KEY_NAME
            )

            self.power_bi_bastion = ec2.Instance(
                self,
                BASTION_NAME,
                instance_name=BASTION_NAME,
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.M5A, ec2.InstanceSize.LARGE
                ),
                require_imdsv2=True,
                detailed_monitoring=True,
                ebs_optimized=True,
                machine_image=ec2.MachineImage.latest_windows(
                    version=ec2.WindowsVersion.WINDOWS_SERVER_2022_SPANISH_FULL_BASE
                ),
                vpc=tenant_vpc,
                security_group=self.bastion_security_group,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                key_pair=self.bastion_key,
                ssm_session_permissions=True,
                associate_public_ip_address=True,
                block_devices=[
                    ec2.BlockDevice(
                        device_name="/dev/sda1",
                        volume=ec2.BlockDeviceVolume.ebs(
                            volume_type=ec2.EbsDeviceVolumeType.GP3,
                            volume_size=volume_size,
                            delete_on_termination=True,
                            encrypted=True,
                        ),
                    )
                ],
            )
