# region: primitives
from constructs import Construct
# endregion


# region: aws-cdk
import aws_cdk as core
from aws_cdk import RemovalPolicy, Aws
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer
from aws_cdk.aws_s3 import Bucket, LifecycleRule
import aws_cdk.aws_glue as glue
import aws_cdk.aws_athena as athena
# endregion

# region: morales cdk-pug-platform
from cdk_pug_platform.models.tenants.tenant_base import TenantBase
# endregion


class ServiceLoadBalancerLoggingBuilder(Construct):
    def _build_load_balancer_logging(
        self,
        tenant: TenantBase
    ):
        ALB_LOGS_BUCKET_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-alb-logs-bucket"
        )

        self.alb_logs_bucket = Bucket(
            self,
            ALB_LOGS_BUCKET_NAME,
            bucket_name=ALB_LOGS_BUCKET_NAME,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
            lifecycle_rules=[
                LifecycleRule(
                    expiration=core.Duration.days(30)
                )
            ]
        )

        ALB_LOGS_DATABASE_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-alb-logs-db"
        )

        self.alb_logs_db = glue.CfnDatabase(
            self,
            ALB_LOGS_DATABASE_NAME,
            catalog_id=Aws.ACCOUNT_ID,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name=ALB_LOGS_DATABASE_NAME
            )
        )

        ALB_LOGS_WORKGROUP_NAME = (
            f"{tenant.COMPANY}-{tenant.ENVIRONMENT.value}-alb-logs-workgroup"
        )

        self.athena_workgroup = athena.CfnWorkGroup(
            self,
            ALB_LOGS_WORKGROUP_NAME,
            name=ALB_LOGS_WORKGROUP_NAME,
            work_group_configuration=(
                athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                    result_configuration=(
                        athena.CfnWorkGroup.ResultConfigurationProperty(
                            output_location=(
                                f"s3://{self.alb_logs_bucket.bucket_name}"
                                f"/athena-results/"
                            )
                        )
                    )
                )
            )
        )

    def _build_log_access_logs(
        self,
        alb: ApplicationLoadBalancer,
        service_name: str
    ):
        alb.log_access_logs(
            self.alb_logs_bucket,
            prefix=service_name
        )

        self._create_glue_table(service_name)

    def _create_glue_table(self, service_name: str):
        ALB_LOGS_TABLE_NAME = (
            f"{service_name}-alb-logs-table"
        )
        glue.CfnTable(
            self,
            ALB_LOGS_TABLE_NAME,
            catalog_id=Aws.ACCOUNT_ID,
            database_name=self.alb_logs_db.ref,
            table_input=glue.CfnTable.TableInputProperty(
                name=ALB_LOGS_TABLE_NAME,
                table_type="EXTERNAL_TABLE",
                parameters={
                    "classification": "csv",
                    "typeOfData": "file",
                    "serialization.format": "1",
                    "input.regex": (
                        r'([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) '  # noqa
                        r'([-.\d]*) ([-.\d]*) ([-.\d]*) (|[-\d]*) (-|[-\d]*) '
                        r'([-\d]*) ([-\d]*) \"([^ ]*) (.*) (- |[^ ]*)\" \"([^\"]*)\" '  # noqa
                        r'([A-Z0-9-_]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" '  # noqa
                        r'\"([^\"]*)\" ([-.\d]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" '  # noqa
                        r'\"([^ ]*)\" \"([^\\s]+?)\" \"([^\\s]+)\" \"([^ ]*)\" \"([^ ]*)\" ?([^ ]*)?'  # noqa
                    ),
                    "projection.enabled": "true",
                    "projection.day.type": "date",
                    "projection.day.range": "2022/01/01,NOW",
                    "projection.day.format": "yyyy/MM/dd",
                    "projection.day.interval": "1",
                    "projection.day.interval.unit": "DAYS",
                    "storage.location.template": (
                        f"s3://{self.alb_logs_bucket.bucket_name}/"
                        f"{service_name}/AWSLogs/{Aws.ACCOUNT_ID}/elasticloadbalancing/"  # noqa
                        f"{Aws.REGION}/${{day}}"
                    ),
                },
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    columns=[
                        glue.CfnTable.ColumnProperty(
                            name="type", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="time", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="elb", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="client_ip", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="client_port", type="int"),
                        glue.CfnTable.ColumnProperty(
                            name="target_ip", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="target_port", type="int"),
                        glue.CfnTable.ColumnProperty(
                            name="request_processing_time", type="double"),
                        glue.CfnTable.ColumnProperty(
                            name="target_processing_time", type="double"),
                        glue.CfnTable.ColumnProperty(
                            name="response_processing_time", type="double"),
                        glue.CfnTable.ColumnProperty(
                            name="elb_status_code", type="int"),
                        glue.CfnTable.ColumnProperty(
                            name="target_status_code", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="received_bytes", type="bigint"),
                        glue.CfnTable.ColumnProperty(
                            name="sent_bytes", type="bigint"),
                        glue.CfnTable.ColumnProperty(
                            name="request_verb", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="request_url", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="request_proto", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="user_agent", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="ssl_cipher", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="ssl_protocol", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="target_group_arn", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="trace_id", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="domain_name", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="chosen_cert_arn", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="matched_rule_priority", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="request_creation_time", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="actions_executed", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="redirect_url", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="lambda_error_reason", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="target_port_list", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="target_status_code_list", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="classification", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="classification_reason", type="string"),
                        glue.CfnTable.ColumnProperty(
                            name="conn_trace_id", type="string"),
                    ],
                    location=(
                        f"s3://{self.alb_logs_bucket.bucket_name}/"
                        f"{service_name}/AWSLogs/{Aws.ACCOUNT_ID}/"
                        f"elasticloadbalancing/{Aws.REGION}/"
                    ),
                    input_format="org.apache.hadoop.mapred.TextInputFormat",
                    output_format=(
                        "org.apache.hadoop.hive.ql.io."
                        "HiveIgnoreKeyTextOutputFormat"
                    ),
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library=(
                            "org.apache.hadoop.hive.serde2.RegexSerDe"
                        ),
                        parameters={"serialization.format": "1"}
                    )
                )
            )
        )
