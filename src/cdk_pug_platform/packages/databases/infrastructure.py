from enum import Enum

from aws_cdk import (
    aws_ec2 as ec2,
    CfnOutput,
    aws_rds as rds,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_sqs as sqs,
    aws_route53 as route53,
)

from constructs import Construct

from cdk_pug_platform.models.environments.app_environment import AppEnvironment
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.packages.federated_dns.infrastructure import FederatedDns


class Databases(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        tenant_vpc: ec2.Vpc,
        database_instances: list[Enum],
        tenant_dns: FederatedDns,
        is_unique: bool = False,
        **kwargs,
    ):
        CONSTRUCT_ID = "database" if is_unique else "database-instances"
        super().__init__(scope, CONSTRUCT_ID, **kwargs)
        environment_name = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"
        self._init_shared_resources(environment_name, tenant, tenant_vpc)

        for database_instance in database_instances:
            if is_unique:
                db_name = f"{environment_name}"
            else:
                db_name = f"{environment_name}-{database_instance.value}"

            self._init_rule(db_name, database_instance)
            self._init_security(db_name, tenant, tenant_vpc, database_instance)
            self._init_server(db_name, tenant, database_instance, tenant_dns)

            CFN_OUTPUT_DATABASE = (
                f"database-instance-endpoint-{database_instance.value}"
            )
            CfnOutput(
                self,
                CFN_OUTPUT_DATABASE,
                value=self.db_instances[database_instance].attr_endpoint_address,
                description=CFN_OUTPUT_DATABASE.replace("-", " "),
            )

    def _init_shared_resources(
        self, db_name: str, tenant: TenantBase, tenant_vpc: ec2.Vpc
    ):
        self.db_security_groups: dict[Enum, ec2.SecurityGroup] = {}
        self.event_rules: dict[Enum, events.Rule] = {}
        self.db_instances: dict[Enum, rds.CfnDBInstance] = {}
        self.db_instance_wrappers: dict[Enum, rds.IDatabaseInstance] = {}

        TENANT_ENVIRONMENT_SUBNETS_GROUP_NAME = f"{db_name}-subnets-group"

        DESCRIPTION = f"{db_name.replace("-", " ")} DB subnet group"

        self.tenant_subnets_group = rds.SubnetGroup(
            self,
            TENANT_ENVIRONMENT_SUBNETS_GROUP_NAME,
            subnet_group_name=TENANT_ENVIRONMENT_SUBNETS_GROUP_NAME,
            vpc=tenant_vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=(
                    ec2.SubnetType.PRIVATE_ISOLATED
                    if tenant.ENVIRONMENT is AppEnvironment.LIVE
                    else ec2.SubnetType.PUBLIC
                )
            ),
            description=DESCRIPTION,
        )

        TENANT_ENVIRONMENT_QUEUE_NAME = f"{db_name}-" f"db-factory-queue"

        self.event_queue = sqs.Queue(
            self,
            TENANT_ENVIRONMENT_QUEUE_NAME,
            queue_name=TENANT_ENVIRONMENT_QUEUE_NAME,
        )

        if tenant.ENVIRONMENT is AppEnvironment.LIVE:
            TENANT_ENVIRONMENT_BASTION_SECURITY_GROUP_NAME = (
                f"{db_name}-" f"bastion-security-group"
            )

            self.tenant_bastion_security_group = ec2.SecurityGroup(
                self,
                TENANT_ENVIRONMENT_BASTION_SECURITY_GROUP_NAME,
                security_group_name=(TENANT_ENVIRONMENT_BASTION_SECURITY_GROUP_NAME),
                vpc=tenant_vpc,
                allow_all_outbound=True,
            )

            self._init_bastion(db_name, tenant_vpc)

    def _init_bastion(self, db_name: str, tenant_vpc: ec2.Vpc):
        TENANT_ENVIRONMENT_BASTION_NAME = f"{db_name}-bastion"

        self.tenant_bastion = ec2.BastionHostLinux(
            self,
            TENANT_ENVIRONMENT_BASTION_NAME,
            instance_name=TENANT_ENVIRONMENT_BASTION_NAME,
            vpc=tenant_vpc,
            security_group=self.tenant_bastion_security_group,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

    def _init_security(
        self,
        db_name: str,
        tenant: TenantBase,
        tenant_vpc: ec2.Vpc,
        database_instance: Enum,
    ):
        TENANT_ENVIRONMENT_DB_SECURITY_GROUP_NAME = f"{db_name}-db-security-group"

        self.db_security_groups[database_instance] = ec2.SecurityGroup(
            self,
            TENANT_ENVIRONMENT_DB_SECURITY_GROUP_NAME,
            security_group_name=TENANT_ENVIRONMENT_DB_SECURITY_GROUP_NAME,
            vpc=tenant_vpc,
            allow_all_outbound=True,
        )

        if tenant.ENVIRONMENT is AppEnvironment.LIVE:
            self.db_security_groups[database_instance].add_ingress_rule(
                peer=self.tenant_bastion_security_group,
                connection=ec2.Port.tcp(
                    tenant.rds_blueprints[database_instance].capacity.port
                ),
                description="Allow database_instance access from bastion host",
            )

    def _init_server(
        self,
        db_name: str,
        tenant: TenantBase,
        database_instance: Enum,
        tenant_dns: FederatedDns,
    ):
        TENANT_ENVIRONMENT_DATABASE_NAME = f"{db_name}-db-server"

        """
        TL; DR: db_name parameter is not supported with SQL Server Express
        because it is not supported by the RDS service
        besides with the factory we can initialize N database_instances
        with different service user names and passwords for each database_instance
        givin the less privilege possible to the service user
        TODO: the hight goal is rotate the service password each day with the minimum impact possible
        this goal is to reduce the possible access to the db with service user
        and if the password is compromised the impact is minimal
        the password is stored in the secret manager and the rotation is done by the secret manager
        event rule detects the password rotation and update the service involved with the new password
        TODO: All database_instance access must include identification and authorization integration with Microsoft Entra.
        TODO: is preferable enroll IAM Identity Center with Microsoft Entra (Azure AD)
        this will reduce the maintenance of the aws users and groups and access to the resources
        besides will reduce the maintenance of the users and passwords in the database_instance
        to reduce the possible errors is mandatory define a group in microsoft entra
        for AWS users integrating AWS in office tools
        besides in the AWS side will apply the least privilege principle
        by groups to reduce the surface of attack and possibility of compromise
        access to the resources
        TODO: investigate the casuistic unauthorized access to AWS detection
        The goal is to detect unauthorized access to AWS resources quickly
        and take the necessary actions to cut permissions automatically
        """  # noqa

        allocated_storage = tenant.rds_blueprints[
            database_instance
        ].capacity.allocated_storage
        self.db_instances[database_instance] = rds.CfnDBInstance(
            self,
            TENANT_ENVIRONMENT_DATABASE_NAME,
            db_instance_identifier=TENANT_ENVIRONMENT_DATABASE_NAME,
            db_subnet_group_name=self.tenant_subnets_group.subnet_group_name,
            vpc_security_groups=[
                self.db_security_groups[database_instance].security_group_id
            ],
            manage_master_user_password=True,
            publicly_accessible=(
                False if tenant.ENVIRONMENT is AppEnvironment.LIVE else True
            ),
            multi_az=False,
            engine=tenant.rds_blueprints[
                database_instance
            ].performance.engine.engine_type,
            engine_version=(
                tenant.rds_blueprints[database_instance].performance.engine.engine_version.full_version  # type: ignore
            ),
            license_model="license-included",
            enable_cloudwatch_logs_exports=["error"],
            storage_type="gp3",
            enable_performance_insights=True,
            master_username="".join(e for e in tenant.COMPANY if e.isalnum()),
            db_instance_class=tenant.rds_blueprints[
                database_instance
            ].performance.instance_type,
            allocated_storage=(f"{allocated_storage}"),
            iops=tenant.rds_blueprints[database_instance].capacity.iops,
            storage_throughput=tenant.rds_blueprints[
                database_instance
            ].capacity.storage_throughput,
        )

        DB_INSTANCE_WRAPPER_NAME = f"{db_name}-wrapper"

        self.db_instance_wrappers[database_instance] = (
            rds.DatabaseInstance.from_database_instance_attributes(
                self,
                DB_INSTANCE_WRAPPER_NAME,
                instance_identifier=self.db_instances[database_instance].ref,
                instance_endpoint_address=(
                    self.db_instances[database_instance].attr_endpoint_address
                ),
                port=tenant.rds_blueprints[database_instance].capacity.port,
                security_groups=[self.db_security_groups[database_instance]],
            )
        )

        if tenant.ENVIRONMENT is not AppEnvironment.LIVE:
            route53.CnameRecord(
                self,
                f"{db_name}-db-cname",
                zone=tenant_dns.main_zone,
                record_name=TENANT_ENVIRONMENT_DATABASE_NAME,
                domain_name=self.db_instances[database_instance].attr_endpoint_address,
            )

        route53.CnameRecord(
            self,
            f"private-{db_name}-db-cname",
            zone=tenant_dns.private_zone,
            record_name=TENANT_ENVIRONMENT_DATABASE_NAME,
            domain_name=self.db_instances[database_instance].attr_endpoint_address,
        )

    def _init_rule(self, db_name: str, database_instance: Enum):
        TENANT_ENVIRONMENT_DB_FACTORY_EVENT_RULE_NAME = (
            f"{db_name}-" f"db-factory-event-rule"
        )

        detail = {
            "SourceType": ["DB_INSTANCE"],
            "SourceIdentifier": [{"prefix": db_name}],
            "EventID": ["RDS-EVENT-0005", "RDS-EVENT-0006"],
        }

        self.event_rules[database_instance] = events.Rule(
            self,
            TENANT_ENVIRONMENT_DB_FACTORY_EVENT_RULE_NAME,
            rule_name=TENANT_ENVIRONMENT_DB_FACTORY_EVENT_RULE_NAME,
            event_pattern=events.EventPattern(
                source=["aws.rds"], detail_type=["RDS DB Instance Event"], detail=detail
            ),
        )

        target = events_targets.SqsQueue(queue=self.event_queue)

        self.event_rules[database_instance].add_target(target)  # type: ignore
