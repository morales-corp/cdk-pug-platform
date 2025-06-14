from aws_cdk import aws_iam as iam, CfnOutput, Aws
from constructs import Construct


class GitHubOidc(Construct):

    def __init__(self, scope: Construct, **kwargs):
        super().__init__(scope, "github-oidc", **kwargs)

        OIDC_PROVIDER_NAME = "github-oidc-provider"

        github_oidc = iam.OpenIdConnectProvider(
            self,
            OIDC_PROVIDER_NAME,
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
            thumbprints=["6938fd4d98bab03faadb97b34396831e3780aea1"],
        )

        assume_role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": github_oidc.open_id_connect_provider_arn
                    },
                    "Action": ["sts:AssumeRoleWithWebIdentity"],
                    "Condition": {
                        "StringEquals": {
                            "token.actions.githubusercontent.com:aud": (
                                "sts.amazonaws.com"
                            )
                        }
                    },
                }
            ],
        }

        ROLE_NAME = "github-actions-role"

        role = iam.CfnRole(
            self,
            ROLE_NAME,
            role_name=ROLE_NAME,
            assume_role_policy_document=assume_role_policy_document,
            description=("IAM Role for GitHub Actions"),
        )

        ECS_DEPLOY_PERMISSIONS_POLICY_NAME = "ecs-deploy-permissions-policy"
        account_arn = f"arn:aws:ecs:{Aws.REGION}:{Aws.ACCOUNT_ID}"
        iam.CfnPolicy(
            self,
            ECS_DEPLOY_PERMISSIONS_POLICY_NAME,
            policy_name=ECS_DEPLOY_PERMISSIONS_POLICY_NAME,
            roles=[role.ref],
            policy_document={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "EcsDeployPermissions",
                        "Effect": "Allow",
                        "Action": [
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
                        "Resource": [
                            (
                                f"{account_arn}:service"
                                "/*-*-ecs-cluster"
                                "/*-*-*-container-service"
                            ),
                            (f"{account_arn}:cluster" "/*-*-ecs-cluster"),
                            (f"{account_arn}:task-definition/*"),
                        ],
                    }
                ],
            },
        )

        OUTPUT_NAME = "github-actions-role-arn"

        CfnOutput(
            self,
            OUTPUT_NAME,
            value=github_oidc.open_id_connect_provider_arn,
            description="IAM Role ARN created for GitHub Actions",
        )
