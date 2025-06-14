from constructs import Construct

import aws_cdk as core
from aws_cdk import (
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
)

from cdk_pug_platform.models.compute.operating_system import OperatingSystem
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class InstanceKeyPair(Construct):
    def __init__(
        self,
        scope: Construct,
        stack_id: str,
        operating_system: OperatingSystem,
        **kwargs,
    ):
        ENVIRONMENT_NAME = f"{stack_id}-{operating_system.value.lower()}"
        super().__init__(scope, f"{ENVIRONMENT_NAME}-key-pair", **kwargs)

        self.so_key_pair_generation(
            operating_system=operating_system, environment_name=ENVIRONMENT_NAME
        )

    def so_key_pair_generation(
        self, operating_system: OperatingSystem, environment_name: str
    ):
        KEY_NAME = f"{environment_name}-key-pair"
        SECRET_NAME = f"{environment_name}-key-pair-private"
        private_key = (
            rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            if operating_system == OperatingSystem.WINDOWS
            else ed25519.Ed25519PrivateKey.generate()
        )

        pem_format = (
            serialization.PrivateFormat.TraditionalOpenSSL
            if operating_system == OperatingSystem.WINDOWS
            else serialization.PrivateFormat.PKCS8
        )

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=pem_format,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

        public_key = private_key.public_key()
        public_key_openssh = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        ).decode("utf-8")

        self.key_pair = ec2.KeyPair(
            self,
            KEY_NAME,
            key_pair_name=KEY_NAME,
            public_key_material=public_key_openssh,
        )

        self.key_pair_private_secret = secretsmanager.Secret(
            self,
            SECRET_NAME,
            secret_name=SECRET_NAME,
            secret_string_value=core.SecretValue.unsafe_plain_text(private_key_pem),
        )
