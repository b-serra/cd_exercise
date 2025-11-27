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
lol