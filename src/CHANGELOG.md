# Changelog

## Unreleased (2025-03-07)

### Other

- Set is_db_secret_required to True by default in ECS task and service classes.
    
### Updates

- Refactor service secrets handling to conditionally create database secrets based on configuration.
    
- Update changelog for upcoming release and rename DatabaseConfig to SqlServerDatabaseConfig with detailed cost impact information.
    
## 1.0.44 (2025-03-07)

### Other

- Version updated from 1.0.43 to 1.0.44.
    
### Updates

- Update changelog for upcoming release and rename DatabaseConfig to SqlServerDatabaseConfig with detailed cost impact information.
    

## 1.0.43 (2025-03-07)

### Other

- Version updated from 1.0.42 to 1.0.43.
    
### Updates

- Refactor FactoryDatabases: use dynamic lambda name based on database instance value.
    
- Update changelog for version 1.0.41 and enhance DatabaseMatrix and ApplicationDashboard functionality.
    

## 1.0.42 (2025-03-06)

### Other

- Version updated from 1.0.41 to 1.0.42.
    
- Enhance DatabaseMatrix: add environment-specific matrix seed handling and optional environment parameter to build method.
    
- Enhance ApplicationDashboard: add unique database instance flag, improve service name formatting, and update changelog.
    

## 1.0.41 (2025-03-04)

### Other

- Version updated from 1.0.40 to 1.0.41.
    
- Enhance ApplicationDashboard: add unique database instance flag and improve service name formatting.
    
### Updates

- Update build and versioning process; remove old bumpversion config and add new dependencies.
    

## 1.0.40 (2025-03-04)

### Other

- Version updated from 1.0.39 to 1.0.40.
    

## 1.0.39 (2025-03-04)

### Other

- Version updated from 1.0.38 to 1.0.39.
    
## 1.0.38 (2025-03-04)

### Other

- Version updated from 1.0.37 to 1.0.38.
    
## 1.0.37 (2025-03-04)

### Other

- Version updated from 1.0.36 to 1.0.37.
    
## 1.0.36 (2025-03-04)

### Other

- Version updated from 1.0.35 to 1.0.36.
    
- Enhance firewall rules and Power BI Bastion configuration for live environment.
    
## 1.0.34 (2025-03-04)

### Other

- Version updated from 1.0.33 to 1.0.34.
    
## 1.0.33 (2025-03-04)

### Other

- Version updated from 1.0.32 to 1.0.33.
    
## 1.0.32 (2025-03-03)

### Other

- Version updated from 1.0.31 to 1.0.32.
    
## 1.0.31 (2025-03-03)

### Other

- Version updated from 1.0.30 to 1.0.31.
    
## 1.0.30 (2025-03-03)

### Other

- Version updated from 1.0.29 to 1.0.30.
    
## 1.0.29 (2025-03-03)

### Other

- Version updated from 1.0.28 to 1.0.29.
    
## 1.0.28 (2025-03-03)

### New

- Add OIDC providers support and create IAM resources for pipelines.
    
### Other

- Version updated from 1.0.27 to 1.0.28.
    
## 1.0.27 (2025-03-03)

### Other

- Version updated from 1.0.26 to 1.0.27.
    
## 1.0.26 (2025-03-03)

### Other

- Version updated from 1.0.25 to 1.0.26.
    
## 1.0.25 (2025-03-03)

### Other

- Version updated from 1.0.24 to 1.0.25.
    
## 1.0.24 (2025-03-03)

### Other

- Version updated from 1.0.23 to 1.0.24.
    
## 1.0.23 (2025-03-03)

### Other

- Version updated from 1.0.22 to 1.0.23.
    
## 1.0.22 (2025-03-03)

### Other

- Version updated from 1.0.21 to 1.0.22.
    
## 1.0.21 (2025-03-03)

### Other

- Version updated from 1.0.20 to 1.0.21.
    
## 1.0.20 (2025-03-03)

### Other

- Version updated from 1.0.19 to 1.0.20.
    
## 1.0.19 (2025-03-03)

### Other

- Version updated from 1.0.18 to 1.0.19.
    
## 1.0.18 (2025-03-02)

### Fixes

- Fix import statement for EcsComputeArchitecture in infrastructure.py.
    
### New

- Add override option to load_dotenv for environment variable loading.
    
### Other

- Version updated from 1.0.17 to 1.0.18.
    
## 1.0.17 (2025-03-02)

### Other

- Version updated from 1.0.16 to 1.0.17.
    
### Updates

- Refactor ECS service and database constructors to support explicit compute architecture and unique instance naming.
    
## 1.0.16 (2025-03-02)

### Other

- Version updated from 1.0.15 to 1.0.16.
    
### Updates

- Refactor constructor call in FactoryDatabases for improved readability.
    
## 1.0.15 (2025-03-01)

### New

- Add support for unique database instance naming in infrastructure classes.
    
- Add support for multiple ECS compute architectures in task definitions.
    
### Other

- Version updated from 1.0.14 to 1.0.15.
    
## 1.0.14 (2025-02-28)

### Other

- Version updated from 1.0.13 to 1.0.14.
    
### Updates

- Update platform configuration to use LINUX_ARM64 for container images.
    
- Update default instance size in InstanceSelector to CPU 4 and RAM 16 GB.
    
## 1.0.13 (2025-02-28)

### Other

- Version updated from 1.0.12 to 1.0.13.
    
### Updates

- Update git configuration in user data script to use system-wide settings.
    
- Refactor instance size validation logic and update ARM64 runtime platform configuration.
    
## 1.0.12 (2025-02-28)

### New

- Add support for M7g instance sizes and enhance instance selection logic; update Docker installation script, change ecs fargate to arm.
    
- Add OperationsSizeT4g enum for instance size options and enhance user data script with detailed logging.
    
### Other

- Version updated from 1.0.11 to 1.0.12.
    
- Enhance user data script with improved logging, architecture detection, and user-specific configurations.
    
## 1.0.11 (2025-02-27)

### Other

- Version updated from 1.0.10 to 1.0.11.
    
### Updates

- Refactor deployment configuration by moving IS_FIRST_DEPLOYMENT constant to DeploymentConfig and improving print statements for clarity.
    
## 1.0.10 (2025-02-27)

### Other

- Version updated from 1.0.9 to 1.0.10.
    
### Updates

- Refactor configuration and validation logic by moving constants to a new utils module and enhancing environment validation.
    
- Refactor EcsScheduledTask and EcsService classes for improved parameter handling and default value assignment.
    
## 1.0.9 (2025-02-27)

### Other

- Version updated from 1.0.8 to 1.0.9.
    
### Updates

- Refactor EcsScheduledTask and EcsService classes for improved readability and consistency.
    
## 1.0.8 (2025-02-27)

### Other

- Version updated from 1.0.7 to 1.0.8.
    
### Updates

- Refactor ECS service and scheduled task classes to include unique identifier handling and integrate load balancer logging.
    
## 1.0.7 (2025-02-27)

### New

- Add is_internal parameter to EcsService initialization.
    
### Other

- Version updated from 1.0.6 to 1.0.7.
    
## 1.0.6 (2025-02-27)

### Other

- Version updated from 1.0.5 to 1.0.6.
    
### Updates

- Update build command to use bump2version and remove changelog file.
    
## 1.0.5 (2025-02-27)

### Other

- Version updated from 1.0.4 to 1.0.5.
    
## 1.0.4 (2025-02-27)

### Fixes

- Fix key pair naming convention in PowerBiBastion to use lowercase for operating system.
    
### New

- Add MSSQL_PORT constant for SQL Server configuration.
    
- Add cryptography and python-dotenv dependencies to pyproject.toml.
    
- Add instance_name parameter to InstanceOperations for clarity.
    
- Add devcontainer configuration and installation script; update volume size in InstanceOperations.
    
- Add docstring to PowerBiBastion class to clarify its purpose and security considerations.
    
- Add OneTimeEc2ConfigStack for initial EC2 key pair setup; refactor PlaygroundStack to remove first deployment flag and streamline PowerBiBastion configuration.
    
- Add PowerBiBastion class for managing Power BI bastion host setup; update PlaygroundStack to integrate networking and PowerBiBastion components; modify CIDR constants and remove unnecessary dependencies in VSCode tasks.
    
- Add IAC_LEAD_HOME_CIDR constant and fix typo in PlaygroundStack initialization; update TenantOrigenCorp to include new CIDR.
    
- Add PlaygroundStack class to manage playground environment setup in AWS CDK.
    
- Add ORIGEN_CORP_CIDR constant and update TenantOrigenCorp to include CIDR in prefix list.
    
- Add cryptography support for PowerBiBastion class to manage private key generation and storage in Secrets Manager.
    
- Add PowerBiBastion class to manage Power BI bastion host setup with security group and key pair.
    
- Add PrefixListCidr class and update TenantBase to include prefix list CIDRs; refactor networking infrastructure to use dynamic entries.
    
### Other

- Version updated from 1.0.3 to 1.0.4.
    
- Version updated from 1.0.3 to 1.0.4.
    
- Version updated from 1.0.2 to 1.0.3.
    
- Version updated from 1.0.1 to 1.0.2.
    
- Version updated from 1.0.1 to 1.0.2.
    
- Version updated from 1.0.0 to 1.0.1.
    
- Enhance EcsFargateServiceParams to support internal services and update hosted zone handling; add new EcsService class for EFS compatibility; bump version to 1.1.6 in pyproject.toml.
    
- Set IS_FIRST_DEPLOYMENT to False in PlaygroundStack for subsequent deployments.
    
### Updates

- Update changelog configuration and versioning format.
    
- Refactor public_hosted_zone type to IHostedZone and update service parameters in ECS Fargate service.
    
- Remove obsolete changelog configuration file.
    
- Update versioning configuration to reflect cdk_pug_platform module and add bumpversion configuration file.
    
- Refactor code for improved readability: add new __init__.py file, update requirements to include generate-changelog, and clean up code formatting across multiple files.
    
- Refactor ECS service infrastructure: add ServiceTaskDefinitionBuilder, update EcsService to integrate task definition building, and remove deprecated ecs_service_v2 module renaming to ecs_service; update requirements for cryptography and python-dotenv.
    
- Refactor service builders to remove is_first_deployment parameter; integrate dotenv for environment variable management; update secret parsing logic; add constants for deployment checks.
    
- Refactor ServiceSecretsBuilder and ApplicationMonitoring to remove is_first_deployment parameter; update related methods to use dot_config_relative_path instead; bump version to 1.1.7 in pyproject.toml.
    
- Refactor EcsFargateServiceParams to rename public_hosted_zone to hosted_zone and update certificate to be optional; bump version to 1.1.1 in pyproject.toml.
    
- Update default stack ID and integrate Networking and InstanceOperations in TenantStack.
    
- Remove unused components from PlaygroundStack and add placeholder for testing purposes.
    
- Update directory creation paths in scripts to use home directory.
    
- Update task label in VSCode configuration and bump version to 1.1.0 in pyproject.toml.
    
- Update InstanceOperations to use Linux OS; modify security group rules for SSH access and adjust AMI lookup method.
    
- Update devcontainer configuration for Ubuntu 24.04; enhance install script with ECR helper and dotnet SDK installation.
    
- Refactor key pair naming in InstanceOperations and PowerBiBastion to use lowercase for operating system; add RDP ingress rule for bastion security group.
    
- Remove unused prefix list parameter from PlaygroundStack and PowerBiBastion; clean up ingress rule for RDP access.
    
- Update PlaygroundStack for first deployment flag; enhance PowerBiBastion configuration with additional instance settings and EBS volume specifications.
    
- Update PowerBiBastion instance type from MICRO to LARGE for improved performance.
    
- Update AWS CodeArtifact login commands to use 'twine' and add product description to constants.
    
- Refactor import statements for consistency and clarity across multiple modules.
    
- Refactor log title generation to exclude DB instance names from service names for clarity.
    
## 1.0.0 (2025-02-27)

### New

- Add flake8 and pep8 configuration files; update VSCode tasks for line length and refactor code for consistency.
    
- Add initial project structure and configuration files.
    
### Other

- Initial commit.
    
### Updates

- Refactor import statements and clean up code formatting for consistency across modules.
    
- Refactor import paths to use 'cdk_pug_platform' namespace for consistency across modules.
    
- Refactor import paths to use 'libraries' namespace for consistency across modules.
    
- Update VSCode tasks and application code for live environment configuration.
    
- Rename CDK_PUG_PLATFORM to PRODUCT for consistency across the codebase.
    
- Update VSCode tasks to use 'stackId' for stack identification and streamline PYTHONPATH.
    
- Refactor imports to use the new package structure and update requirements.
    

