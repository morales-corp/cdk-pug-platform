# region: primitives
from constructs import Construct
from typing import Optional

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: origen cdk-pug-platform
from cdk_pug_platform.models.iam.oidc_providers import OidcProviders
from cdk_pug_platform.packages.iam.bitbucket_oidc.infrastructure import (
    BitBucketOidc,
    BitBucketOidcParams,
)
from cdk_pug_platform.packages.iam.github_oidc.infrastructure import GitHubOidc

# endregion


class OidcParams:
    def __init__(self, provider: OidcProviders, config: Optional[dict] = None):
        self.provider = provider
        self.config = config


class OneTimePipelinesIamStack(Stack):
    """OneTimePipelinesIamStack
    This stack is responsible for creating the IAM resources for the OneTimePipelines.
    """

    def __init__(
        self,
        scope: Construct,
        oidc_params: list[OidcParams],
        company: Optional[str],
        **kwargs,
    ):
        stack_id = (
            f"one-time-pipelines-iam-{company}" if company else "one-time-pipelines-iam"
        )
        super().__init__(scope, stack_id, **kwargs)

        for param in oidc_params:
            provider = param.provider
            if provider == OidcProviders.GITHUB:
                GitHubOidc(self)
            elif provider == OidcProviders.BITBUCKET:
                if param.config:
                    workspace = param.config["workspace"]
                    workspace_id = param.config["workspace_id"]
                    bitbucket_params = BitBucketOidcParams(
                        workspace=workspace, workspace_id=workspace_id
                    )
                else:
                    raise ValueError("Bitbucket OIDC provider requires a configuration")
                BitBucketOidc(self, bitbucket_params)
            else:
                raise ValueError(f"Invalid OIDC provider: {param.provider.value}")
