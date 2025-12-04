#!/bin/bash

set -e

echo "🚀 Starting Docker & Docker Compose installation..."

# Step 1: Remove old versions
echo "🔍 Removing old Docker versions (if any)..."
sudo apt remove -y docker docker-engine docker.io containerd runc || true

# Step 2: Install dependencies
echo "📦 Installing required packages..."
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

# Step 3: Add Docker GPG key
echo "🔑 Adding Docker’s official GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Step 4: Set up the Docker repo
echo "📝 Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 5: Update apt and install Docker
echo "🚚 Installing Docker Engine and Compose plugin..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 6: Verify installation
echo "✅ Verifying Docker installation..."
docker --version
docker compose version

# Step 7 (optional): Add current user to 'docker' group
echo "👤 Adding current user to 'docker' group (optional)..."
sudo usermod -aG docker $USER

echo "🎉 Docker and Docker Compose installed successfully!"
echo "👉 Please log out and log back in OR run: newgrp docker"
