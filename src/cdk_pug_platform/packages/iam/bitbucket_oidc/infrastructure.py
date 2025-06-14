from aws_cdk import (
    Aws,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class BitBucketOidcParams:
    def __init__(self, workspace: str, workspace_id: str):
        self.workspace = workspace
        self.workspace_id = workspace_id


class BitBucketOidc(Construct):

    def __init__(self, scope: Construct, params: BitBucketOidcParams, **kwargs):
        construct_id = f"{params.workspace}-bitbucket-oidc"
        BITBUCKET_URL = f"https://api.bitbucket.org/2.0/workspaces/{params.workspace}/pipelines-config/identity/oidc"  # noqa

        super().__init__(scope, construct_id, **kwargs)

        OIDC_PROVIDER_NAME = "bitbucket-oidc-provider"

        bitbucket_oidc = iam.OpenIdConnectProvider(
            self,
            OIDC_PROVIDER_NAME,
            url=BITBUCKET_URL,
            client_ids=[
                f"ari:cloud:bitbucket::workspace/{params.workspace_id}",  # noqa
            ],
            thumbprints=["a031c46782e6e6c662c2c87c76da9aa62ccabd8e"],
        )

        ROLE_NAME = "bitbucket-pipelines-role"

        role = iam.Role(
            self,
            ROLE_NAME,
            role_name=ROLE_NAME,
            assumed_by=iam.FederatedPrincipal(
                federated=bitbucket_oidc.open_id_connect_provider_arn,
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),  # type: ignore
            description=("IAM Role for BitBucket Pipelines from any"),
        )

        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess")
        )

        ECS_DEPLOY_PERMISSIONS_POLICY_NAME = "ecs-deploy-permissions-policy"
        account_arn = f"arn:aws:ecs:{Aws.REGION}:{Aws.ACCOUNT_ID}"

        iam.Policy(
            self,
            ECS_DEPLOY_PERMISSIONS_POLICY_NAME,
            policy_name=ECS_DEPLOY_PERMISSIONS_POLICY_NAME,
            roles=[role],
            document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["ecs:ListTaskDefinitions"], resources=["*"]
                    ),
                    iam.PolicyStatement(
                        actions=[
                            "ecs:UpdateService",
                            "ecs:DescribeServices",
                            "ecs:ListServices",
                            "ecs:ListTasks",
                            "ecs:RegisterTaskDefinition",
                            "ecs:RunTask",
                            "ecs:DescribeTasks",
                            "ecs:DescribeTaskDefinition",
                            "ecs:ListTaskDefinitions",
                        ],
                        resources=[
                            (
                                f"{account_arn}:service"
                                "/*-*-ecs-cluster"
                                "/*-*-*-container-service"
                            ),
                            (f"{account_arn}:cluster" "/*-*-ecs-cluster"),
                            (f"{account_arn}:task-definition/*"),
                        ],
                    ),
                    iam.PolicyStatement(
                        actions=["ecr:GetAuthorizationToken"], resources=["*"]
                    ),
                    iam.PolicyStatement(
                        actions=[
                            "ecr:*",
                        ],
                        resources=[
                            f"arn:aws:ecr:{Aws.REGION}:{Aws.ACCOUNT_ID}:repository/*"
                        ],
                    ),
                ]
            ),
        )

        OUTPUT_NAME = "github-actions-role-arn"

        CfnOutput(
            self,
            OUTPUT_NAME,
            value=bitbucket_oidc.open_id_connect_provider_arn,
            description="ARN of the IAM Role created for BitBucket Pipelines",  # noqa
        )
