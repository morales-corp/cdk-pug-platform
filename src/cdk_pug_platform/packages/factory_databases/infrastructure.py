from enum import Enum

# region: aws-cdk
from constructs import Construct
from aws_cdk import (
    Aws,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_ec2 as ec2,
)

# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
from cdk_pug_platform.models.database.database_matrix import _MatrixType
from cdk_pug_platform.modules.docker_lambda.infrastructure import (
    DockerLambdaParams,
    DockerLambdaPug,
)
from cdk_pug_platform.modules.events.lambda_source.infrastructure import (
    LambdaSourceParams,
    LambdaSourcePug,
)
from cdk_pug_platform.modules.private.permission_actions.secrets import (
    GetSecretPermissionAction,
    UpdateSecretPermissionAction,
)
from cdk_pug_platform.modules.private.permission_actions.ecs_services import (
    UpdateServicePermissionAction,
)
from cdk_pug_platform.modules.private.add_to_role_lambda.infrastructure import (
    AddToRoleLambdaParams,
    AddToRoleLambdaPug,
)
from cdk_pug_platform.packages.databases.infrastructure import Databases

# endregion


class FactoryDatabases(Construct):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        tenant_vpc: ec2.Vpc,
        database_instances: list[Enum],
        database_matrix: _MatrixType,
        stack_databases: Databases,
        is_unique: bool = False,
        **kwargs,
    ):
        self.lambda_functions: dict[str, lambda_.IFunction] = {}
        tenant_lambda_security_groups: dict[str, ec2.SecurityGroup] = {}
        for database_instance in database_instances:
            environment_name = f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}"

            if is_unique:
                CONSTRUCT_ID = "database-factory"
                db_instance_name = environment_name
                lambda_name = "db-factory"
            else:
                CONSTRUCT_ID = f"database-{database_instance.value}-factory"
                db_instance_name = f"{environment_name}-{database_instance.value}"
                lambda_name = f"{database_instance.value}-db-factory"

            super().__init__(scope, CONSTRUCT_ID, **kwargs)
            vector_persistent_services = database_matrix.get(database_instance)
            if vector_persistent_services is None:
                continue

            for (
                persistent_database,
                database_with_secrets,
            ) in vector_persistent_services.items():
                persistent_db_name = f"{db_instance_name}-{persistent_database.value}"
                TENANT_ENVIRONMENT_LAMBDA_SECURITY_GROUP_NAME = (
                    f"{persistent_db_name}-db-factory-sg"
                )

                tenant_lambda_security_groups[persistent_db_name] = ec2.SecurityGroup(
                    self,
                    TENANT_ENVIRONMENT_LAMBDA_SECURITY_GROUP_NAME,
                    security_group_name=TENANT_ENVIRONMENT_LAMBDA_SECURITY_GROUP_NAME,
                    vpc=tenant_vpc,
                    allow_all_outbound=True,
                )

                stack_databases.db_security_groups[database_instance].add_ingress_rule(
                    peer=tenant_lambda_security_groups[persistent_db_name],
                    connection=ec2.Port.tcp(
                        tenant.rds_blueprints[database_instance].capacity.port
                    ),
                    description=f"Allow {database_instance.value} factory to connect to the database",
                )

                lambda_environment = {
                    "QUEUE_URL": stack_databases.event_queue.queue_url,
                    "TENANT": tenant.COMPANY,
                    "PRODUCT": tenant.PRODUCT.value,
                    "PERSISTENT_DATABASE": persistent_database.value,
                    "ENVIRONMENT": tenant.ENVIRONMENT.value,
                    "DB_HOST": stack_databases.db_instances[
                        database_instance
                    ].attr_endpoint_address,
                    "DB_PORT": stack_databases.db_instances[
                        database_instance
                    ].attr_endpoint_port,
                    "MASTER_DB_SECRET_ARN": (
                        stack_databases.db_instances[
                            database_instance
                        ].attr_master_user_secret_secret_arn
                    ),
                    "RECREATE_DATABASE": "false",
                    "RECREATE_PASSWORDS": "false",
                    "SERVICES": ",".join(
                        service.name for service in database_with_secrets.keys()
                    ),
                }

                for service, service_user_secret in database_with_secrets.items():
                    lambda_environment[f"{service.name}_SERVICE_USER_SECRET"] = (
                        service_user_secret.model_dump_json()
                    )

                lambda_params = DockerLambdaParams(
                    relative_path="src/services/apps/ms-sql-database-factory",
                    lambda_name=lambda_name,
                    tenant_vpc=tenant_vpc,
                    lambda_environment=lambda_environment,
                    vpc_subnets=ec2.SubnetSelection(
                        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                    ),
                    security_groups=[tenant_lambda_security_groups[persistent_db_name]],
                )

                lambda_pug = DockerLambdaPug(self, tenant, lambda_params)

                self.lambda_functions[persistent_db_name] = lambda_pug.play()

                arn_resources = [
                    secret.secret_arn for secret in database_with_secrets.values()
                ]
                permission_actions = [
                    GetSecretPermissionAction(),
                    UpdateSecretPermissionAction(),
                ]
                add_to_role_lambda_params = AddToRoleLambdaParams(
                    objective="update-secrets",
                    lambda_function=self.lambda_functions[persistent_db_name],
                    permission_actions=permission_actions,
                    arn_resources=arn_resources,
                )

                self.lambda_functions[persistent_db_name] = AddToRoleLambdaPug(
                    add_to_role_lambda_params
                ).play()

                permission_actions = [GetSecretPermissionAction()]

                arn_resources = [
                    stack_databases.db_instances[
                        database_instance
                    ].attr_master_user_secret_secret_arn
                ]

                add_to_role_lambda_params = AddToRoleLambdaParams(
                    objective="get-master-secret",
                    lambda_function=self.lambda_functions[persistent_db_name],
                    permission_actions=permission_actions,
                    arn_resources=arn_resources,
                )

                self.lambda_functions[persistent_db_name] = AddToRoleLambdaPug(
                    add_to_role_lambda_params
                ).play()

                arn_resources = [f"arn:aws:ecs:{Aws.REGION}:{Aws.ACCOUNT_ID}:service/*"]
                permission_actions = [UpdateServicePermissionAction()]

                add_to_role_lambda_params = AddToRoleLambdaParams(
                    objective="update-services",
                    lambda_function=self.lambda_functions[persistent_db_name],
                    permission_actions=permission_actions,
                    arn_resources=arn_resources,
                )

                self.lambda_functions[persistent_db_name] = AddToRoleLambdaPug(
                    add_to_role_lambda_params
                ).play()

                lambda_source_params = LambdaSourceParams(
                    source=lambda_event_sources.SqsEventSource(
                        stack_databases.event_queue, batch_size=1
                    ),
                    lambda_function=self.lambda_functions[persistent_db_name],
                )

                self.lambda_functions[persistent_db_name] = LambdaSourcePug(
                    lambda_source_params
                ).play()
