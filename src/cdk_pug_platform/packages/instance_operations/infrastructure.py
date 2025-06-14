from enum import Enum
from constructs import Construct

from aws_cdk import (
    aws_ec2 as ec2,
)

from cdk_pug_platform.models.compute.operating_system import OperatingSystem
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.packages.instance_operations.scripts import user_data_script


class OperationsSizeT4g(Enum):
    CPU_2_RAM_2_GB = ec2.InstanceSize.SMALL
    CPU_2_RAM_4_GB = ec2.InstanceSize.MEDIUM
    CPU_2_RAM_8_GB = ec2.InstanceSize.LARGE
    CPU_4_RAM_16_GB = ec2.InstanceSize.XLARGE


class OperationsSizeM7g(Enum):
    CPU_2_RAM_4_GB = ec2.InstanceSize.MEDIUM
    CPU_2_RAM_8_GB = ec2.InstanceSize.LARGE
    CPU_4_RAM_16_GB = ec2.InstanceSize.XLARGE


class InstanceSelector:
    def __init__(self, family: ec2.InstanceClass):
        self.family = family
        self.size_type = None

    def size(self, size: Enum):
        if (
            self.family == ec2.InstanceClass.T4G
            and not isinstance(size, OperationsSizeT4g)
        ) or (
            self.family == ec2.InstanceClass.M7G
            and not isinstance(size, OperationsSizeM7g)
        ):
            raise ValueError("Invalid size for the selected instance family")
        self.size_type = size
        return self

    def __repr__(self):
        if not self.size_type:
            raise ValueError("Size must be set before using InstanceSelector")
        return f"InstanceSelector(family={self.family.value}, size={self._size.name})"


default_instance_selector = InstanceSelector(ec2.InstanceClass.T4G).size(
    OperationsSizeT4g.CPU_4_RAM_16_GB
)


class InstanceOperations(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        tenant_vpc: ec2.Vpc,
        prefix_list: ec2.PrefixList,
        volume_size: int = 100,
        instance_selector: InstanceSelector = default_instance_selector,
        **kwargs,
    ):
        super().__init__(scope, "instance-operations", **kwargs)

        environment_name = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"
        INSTANCE_OPERATIONS_SECURITY_GROUP_NAME = (
            f"{environment_name}-instance-operations-security-group"
        )
        INSTANCE_OPERATIONS_NAME = f"{environment_name}-instance-operations"
        operating_system: OperatingSystem = OperatingSystem.LINUX

        self.instance_operations_security_group = ec2.SecurityGroup(
            self,
            INSTANCE_OPERATIONS_SECURITY_GROUP_NAME,
            vpc=tenant_vpc,
            security_group_name=INSTANCE_OPERATIONS_SECURITY_GROUP_NAME,
            description="Instance Operations Security Group",
            allow_all_outbound=True,
        )

        self.instance_operations_security_group.add_ingress_rule(
            ec2.Peer.ipv4(tenant_vpc.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow SSH from Session Manager",
        )

        self.instance_operations_security_group.add_ingress_rule(
            ec2.Peer.prefix_list(prefix_list.prefix_list_id),
            ec2.Port.tcp(22),
            "Allow SSH from Prefix List",
        )

        KEY_NAME = f"{tenant.COMPANY}-{operating_system.value.lower()}-key-pair"

        self.linux_key = ec2.KeyPair.from_key_pair_name(
            self, KEY_NAME, key_pair_name=KEY_NAME
        )

        ubuntu_ami = ec2.MachineImage.from_ssm_parameter(
            parameter_name="/aws/service/canonical/ubuntu/server/24.04/stable/current/arm64/hvm/ebs-gp3/ami-id",
            os=ec2.OperatingSystemType.LINUX,
        )

        self.instance_operations = ec2.Instance(
            self,
            INSTANCE_OPERATIONS_NAME,
            instance_name=INSTANCE_OPERATIONS_NAME,
            instance_type=ec2.InstanceType.of(
                instance_selector.family, instance_selector.size_type.value
            ),
            require_imdsv2=True,
            detailed_monitoring=True,
            ebs_optimized=True,
            machine_image=ubuntu_ami,
            vpc=tenant_vpc,
            security_group=self.instance_operations_security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_pair=self.linux_key,
            ssm_session_permissions=True,
            associate_public_ip_address=True,
            user_data=ec2.UserData.custom(user_data_script),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                        volume_size=volume_size,
                        encrypted=True,
                    ),
                )
            ],
        )
