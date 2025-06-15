# flake8: noqa

user_data_script = """#!/bin/bash -ex
exec > >(tee /var/log/user-data.log) 2>&1

set -e

# Update packages
sudo apt update -y && sudo apt upgrade -y

# Install necessary dependencies
sudo apt install -y curl unzip git software-properties-common

# Install Docker
if ! command -v docker &> /dev/null; then
    sudo apt install -y docker.io docker-buildx  docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo systemctl status docker
    sudo usermod -aG docker ubuntu
    docker buildx create --name mbuilder
    docker buildx use mbuilder
    docker buildx inspect --bootstrap
else
    echo "Docker is already installed."
fi

# Install Node.js LTS and npm
if ! command -v node &> /dev/null; then
    sudo apt-get install -y nodejs npm
else
    echo "Node.js is already installed."
fi

node -v && npm -v

# Detect system architecture
ARCH=$(uname -m)

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
echo "Checking if zsh is installed..."
if ! command -v zsh &> /dev/null; then
    echo "Installing zsh..."
    sudo apt install -y zsh
else
    echo "Zsh is already installed."
fi

USER_HOME="/home/ubuntu"
ZSH_CUSTOM_PLUGINS="$USER_HOME/.zsh_plugins"
ZSHRC="$USER_HOME/.zshrc"

echo "Setting zsh as the default shell for ubuntu..."
sudo usermod -s "$(which zsh)" ubuntu

mkdir -p "$ZSH_CUSTOM_PLUGINS"

echo "Cloning or updating zsh-completions..."
if [ ! -d "$ZSH_CUSTOM_PLUGINS/zsh-completions" ]; then
    git clone https://github.com/zsh-users/zsh-completions.git "$ZSH_CUSTOM_PLUGINS/zsh-completions"
else
    git -C "$ZSH_CUSTOM_PLUGINS/zsh-completions" pull
fi

echo "Cloning or updating zsh-syntax-highlighting..."
if [ ! -d "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting"
else
    git -C "$ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting" pull
fi

echo "Configuring the .zshrc file for ubuntu..."
touch "$ZSHRC"

if ! grep -q "fpath+=($ZSH_CUSTOM_PLUGINS/zsh-completions/src)" "$ZSHRC"; then
    echo "fpath+=($ZSH_CUSTOM_PLUGINS/zsh-completions/src)" | tee -a "$ZSHRC"
fi
if ! grep -q "autoload -U compinit && compinit" "$ZSHRC"; then
    echo "autoload -U compinit && compinit" | tee -a "$ZSHRC"
fi
if ! grep -q "source $ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" "$ZSHRC"; then
    echo "source $ZSH_CUSTOM_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" | tee -a "$ZSHRC"
fi

echo "Setting correct ownership for ubuntu user..."
sudo chown -R ubuntu:ubuntu "$ZSH_CUSTOM_PLUGINS" "$ZSHRC"

echo "Zsh configured as default shell and plugins activated for ubuntu."


# create folder src/server and src/services/apps
echo "Creating directories src/server and src/services/apps..."
mkdir -p $USER_HOME/src/server
mkdir -p $USER_HOME/src/services/apps
sudo chown -R ubuntu:ubuntu $USER_HOME/src

ls -la $USER_HOME/src

sudo apt install python3.12-venv -y

echo "Directories created."
echo "Configuring git..."
sudo apt-get install -y gh
sudo git config --system user.name "Infrastructuras Cloud"
sudo git config --system user.email "<>"
sudo git config --system credential.helper store
echo "Git configured."

echo "User data script completed."
"""
