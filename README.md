# CD Exercise - GitHub Actions Continuous Deployment

A hands-on exercise for learning Continuous Deployment (CD) pipelines using GitHub Actions. This exercise builds upon CI concepts to teach automated deployment workflows.

## Overview

This repository demonstrates progressive CD pipeline development. Each branch introduces new deployment capabilities, building toward a complete continuous deployment pipeline.

## Learning Path

| Branch | Focus | Description |
|--------|-------|-------------|
| `main` | Foundation | Project structure and basic application |
| `01-docker-build` | Containerization | Building and testing Docker images |
| `02-registry-push` | Registry | Pushing images to GitHub Container Registry |
| `03-staging-deploy` | Staging | Deploying to a staging environment |
| `04-production-deploy` | Production | Manual approval and production deployment |
| `05-rollback` | Recovery | Implementing rollback capabilities |
| `06-complete` | Integration | Complete CD pipeline with all stages |
| `07-azure-deploy` | Cloud Deployment | Real deployment to Azure VM via SSH |

## Project Structure

```
cd_exercise/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py          # Flask application
│       └── health.py        # Health check endpoints
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_health.py
├── .github/
│   └── workflows/
│       └── cd.yml           # CD pipeline (varies by branch)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## Prerequisites

- Python 3.9+
- Docker Desktop
- Git
- GitHub account

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Run the Application

```bash
# Run locally
python -m src.app.main

# Run with Docker
docker build -t cd-exercise .
docker run -p 5000:5000 cd-exercise
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## How to Use This Exercise

1. **Start with `main` branch** - Understand the project structure
2. **Progress through branches sequentially** - Each branch adds new CD capabilities
3. **Examine `.github/workflows/cd.yml`** in each branch to see what changes
4. **Fork and experiment** - Modify the code and observe pipeline behavior

## Branch Details

### main - Foundation
Basic project structure with a Flask API application. No CD pipeline yet.

### 01-docker-build - Containerization
- Build Docker image in GitHub Actions
- Run container tests
- Scan for vulnerabilities with Trivy

### 02-registry-push - Container Registry
- Push images to GitHub Container Registry (GHCR)
- Tag images with commit SHA and branch name
- Implement image versioning

### 03-staging-deploy - Staging Environment
- Deploy to staging environment automatically
- Run smoke tests after deployment
- Environment-specific configurations

### 04-production-deploy - Production with Approvals
- Manual approval gates for production
- Blue-green deployment strategy
- Production health checks

### 05-rollback - Recovery Mechanisms
- Automatic rollback on failure
- Version tracking
- Quick recovery procedures

### 06-complete - Full Pipeline
- Complete CD pipeline with all stages
- Parallel jobs where possible
- Comprehensive deployment strategy

### 07-azure-deploy - Azure VM Deployment
- Real deployment to Azure VM via SSH
- Docker container deployment on cloud infrastructure
- GitHub Container Registry integration

#### Prerequisites for Branch 07

Before running the pipeline on this branch, you must:

1. **Install Azure CLI** on your local machine
2. **Have access to an Azure Service Principal** with permissions to create VMs
3. **Create an Azure VM** with Docker installed
4. **Configure GitHub Secrets** in your repository

#### Step 1: Install Azure CLI

```bash
# macOS
brew install azure-cli

# Ubuntu/Debian
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows (PowerShell)
winget install Microsoft.AzureCLI
```

#### Step 2: Azure Service Principal

You need a Service Principal with the following attributes (provided by instructor):

| Attribute | Description | Example |
|-----------|-------------|---------|
| `appId` | Application (client) ID | `13c5b060-82ec-42bb-94fa-dd57ddeb74db` |
| `password` | Client secret value | `0uw8Q~Cosgwq9y-Fp_...` |
| `tenant` | Azure AD tenant ID | `5ca2bc70-353c-4d1f-b7d7-7f2b2259df68` |

The instructor will provide credentials in this format:
```json
{
  "appId": "<AZURE_CLIENT_ID>",
  "displayName": "BCSAI2025-DEVOPS-STUDENTS-A-SP",
  "password": "<AZURE_CLIENT_SECRET>",
  "tenant": "5ca2bc70-353c-4d1f-b7d7-7f2b2259df68"
}
```

#### Step 3: Create the Azure VM

Run these Azure CLI (`az`) commands to create and configure the VM:

| Command | Description |
|---------|-------------|
| `az login` | Authenticate with Azure using service principal |
| `ssh-keygen` | Generate SSH key pair for VM access |
| `az vm create` | Create the virtual machine |
| `az vm open-port` | Open port 5000 in the firewall |
| `az vm show` | Get VM details (public IP) |
| `ssh` | Connect to VM and install Docker |

```bash
# 1. Login with service principal (use appId, password, tenant from Step 2)
az login --service-principal \
  -u <AZURE_CLIENT_ID> \
  -p <AZURE_CLIENT_SECRET> \
  --tenant 5ca2bc70-353c-4d1f-b7d7-7f2b2259df68

# 2. Generate SSH key pair for VM access
ssh-keygen -t rsa -b 4096 -f ~/.ssh/cd-exercise-vm-key -N "" -C "cd-exercise-vm"

# 3. Create the VM (az vm create)
az vm create \
  --resource-group BCSAI2025-DEVOPS-STUDENTS-A \
  --name cd-exercise-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/cd-exercise-vm-key.pub \
  --public-ip-sku Standard

# 4. Open port 5000 for the application (az vm open-port)
az vm open-port \
  --resource-group BCSAI2025-DEVOPS-STUDENTS-A \
  --name cd-exercise-vm \
  --port 5000 \
  --priority 1010

# 5. Get the VM public IP address (az vm show) - SAVE THIS IP!
az vm show \
  --resource-group BCSAI2025-DEVOPS-STUDENTS-A \
  --name cd-exercise-vm \
  --show-details \
  --query publicIps \
  --output tsv

# 6. Install Docker on the VM via SSH (replace <VM_IP> with the IP from step 5)
ssh -i ~/.ssh/cd-exercise-vm-key azureuser@<VM_IP> "curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker azureuser"
```

#### Step 4: Configure GitHub Secrets

Go to your repository **Settings > Secrets and variables > Actions** and add these secrets:

| Secret Name | Source | How to Get the Value |
|-------------|--------|----------------------|
| `AZURE_CLIENT_ID` | Service Principal `appId` | From Step 2 (instructor provided) |
| `AZURE_CLIENT_SECRET` | Service Principal `password` | From Step 2 (instructor provided) |
| `AZURE_TENANT_ID` | Service Principal `tenant` | `5ca2bc70-353c-4d1f-b7d7-7f2b2259df68` |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription | Run: `az account show --query id -o tsv` |
| `VM_HOST` | VM public IP | From Step 3.5 (`az vm show` output) |
| `VM_USERNAME` | VM admin user | `azureuser` (fixed) |
| `VM_SSH_PRIVATE_KEY` | SSH private key | Run: `cat ~/.ssh/cd-exercise-vm-key` (entire file content) |

#### Step 5: Update Workflow with VM IP

Edit `.github/workflows/cd.yml` and update the `VM_PUBLIC_IP` environment variable with your VM's IP address:

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  VM_PUBLIC_IP: "<YOUR_VM_IP_HERE>"  # Update this!
```

#### Step 6: Run the Pipeline

Once all secrets are configured:

1. Push a commit to the `07-azure-deploy` branch, or
2. Go to **Actions > CD Pipeline > Run workflow** and select branch `07-azure-deploy`

After successful deployment, access the application at: `http://<VM_IP>:5000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |
| `/health/ready` | GET | Readiness probe |
| `/health/live` | GET | Liveness probe |
| `/api/version` | GET | Application version |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/staging/production) | development |
| `PORT` | Server port | 5000 |
| `APP_VERSION` | Application version | 0.1.0 |

## Key CD Concepts Covered

- **Container Building** - Creating reproducible deployment artifacts
- **Container Registry** - Storing and versioning container images
- **Environment Promotion** - Moving code through staging to production
- **Deployment Strategies** - Blue-green, rolling updates
- **Approval Gates** - Manual intervention for critical deployments
- **Health Checks** - Verifying deployment success
- **Rollback** - Recovering from failed deployments

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
