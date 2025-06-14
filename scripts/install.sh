#!/bin/bash
set -e

# Update packages
sudo apt update -y && sudo apt upgrade -y

# Install necessary dependencies
sudo apt install -y curl unzip git software-properties-common

# Install Docker
if ! command -v docker &> /dev/null; then
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
else
    echo "Docker is already installed."
fi

# Detect system architecture
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        ARCH_ECR="linux-amd64"
        ;;
    aarch64)
        ARCH_ECR="linux-arm64"
        ;;
    armv7l)
        ARCH_ECR="linux-arm"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# Get the latest version of amazon-ecr-credential-helper
LATEST_VERSION=$(curl -s https://api.github.com/repos/awslabs/amazon-ecr-credential-helper/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
LATEST_VERSION=${LATEST_VERSION#v}  # Remove 'v' prefix if present

echo "The latest version of amazon-ecr-credential-helper is ${LATEST_VERSION}"

# Define the download URL
DOWNLOAD_URL="https://amazon-ecr-credential-helper-releases.s3.us-east-2.amazonaws.com/${LATEST_VERSION}/${ARCH_ECR}/docker-credential-ecr-login"

echo "Downloading amazon-ecr-credential-helper version ${LATEST_VERSION} for ${ARCH_ECR}..."
curl -L -o docker-credential-ecr-login "${DOWNLOAD_URL}"

# Verify if the file was downloaded correctly
if [ ! -s docker-credential-ecr-login ]; then
    echo "Error: Failed to download the binary. Check the URL or your internet connection."
    rm -f docker-credential-ecr-login
    exit 1
fi

# Install amazon-ecr-credential-helper
sudo mv docker-credential-ecr-login /usr/local/bin/
sudo chmod +x /usr/local/bin/docker-credential-ecr-login

# Verify installation
if ! docker-credential-ecr-login version; then
    echo "Error: Installation failed or the downloaded file is not valid."
    exit 1
fi

echo "Installation completed successfully."

# Configure Docker to use the helper
mkdir -p ~/.docker
cat <<EOF > ~/.docker/config.json
{
  "credHelpers": {
    "public.ecr.aws": "ecr-login"
  }
}
EOF

echo "Installation completed. Try with docker login."

# Install Node.js LTS and npm
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
else
    echo "Node.js is already installed."
fi

node -v && npm -v

# Install AWS CLI v2
AWS_CLI_URL="https://awscli.amazonaws.com/awscli-exe-linux-${ARCH}.zip"
curl -fsSL "$AWS_CLI_URL" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
aws --version

# Install AWS CDK globally
sudo npm install -g aws-cdk
cdk --version

# Verify Python (Ubuntu 24.04 includes Python 3.12)
python3 --version
pip3 --version || sudo apt install -y python3-pip

# Add python alias for 3
if ! command -v python &> /dev/null; then
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
fi

# Install dotnet SDK 8.0
if ! command -v dotnet &> /dev/null; then
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    sudo dpkg -i packages-microsoft-prod.deb
    sudo apt update -y
    sudo apt install -y apt-transport-https
    sudo apt update -y
    sudo apt install -y dotnet-sdk-8.0
    rm -f packages-microsoft-prod.deb
else
    echo "Dotnet SDK 8.0 is already installed."
fi

# Install zsh
if ! command -v zsh &> /dev/null; then
    sudo apt install -y zsh
else
    echo "Zsh is already installed."
fi

zsh --version

# Directory where we will install the plugins
ZSH_CUSTOM_PLUGINS="$HOME/.zsh_plugins"
mkdir -p "$ZSH_CUSTOM_PLUGINS"

# Clone or update zsh-completions
if [ ! -d "$ZSH_CUSTOM_PLUGINS/zsh-completions" ]; then
    git clone https://github.com/zsh-users/zsh-completions.git "$ZSH_CUSTOM_PLUGINS/zsh-completions"
else
    git -C "$ZSH_CUSTOM_PLUGINS/zsh-completions" pull
fi

# Clone or update zsh-syntax-highlighting
if [ ! -d "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting"
else
    git -C "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting" pull
fi

# Ensure .zshrc configurations
if ! grep -q "fpath+=($ZSH_CUSTOM_PLUGINS/zsh-completions/src)" ~/.zshrc; then
    echo "fpath+=($ZSH_CUSTOM_PLUGINS/zsh-completions/src)" >> ~/.zshrc
fi

if ! grep -q "autoload -U compinit && compinit" ~/.zshrc; then
    echo "autoload -U compinit && compinit" >> ~/.zshrc
fi

if ! grep -q "source $ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ~/.zshrc; then
    echo "source $ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
fi

echo "Installation and configuration complete!"
