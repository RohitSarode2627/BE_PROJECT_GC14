# 🚀 End-to-End CI/CD Pipeline Implementation Guide
### Project: Crime Prediction Web Application (`BE_PROJECT_GC14`)
**Tech Stack:** Docker • AWS Free Tier • Terraform • Ansible • GitHub Actions

---

## 📋 Table of Contents
1. [Architecture Overview & Workflow](#1-architecture-overview--workflow)
2. [Prerequisites & Local Tooling](#2-prerequisites--local-tooling)
3. [Recommended Repository Structure](#3-recommended-repository-structure)
4. [Phase 1: Containerization with Docker](#phase-1-containerization-with-docker)
5. [Phase 2: Infrastructure as Code (IaC) with Terraform](#phase-2-infrastructure-as-code-iac-with-terraform)
6. [Phase 3: Configuration Management with Ansible](#phase-3-configuration-management-with-ansible)
7. [Phase 4: CI/CD Automation with GitHub Actions](#phase-4-cicd-automation-with-github-actions)
8. [Phase 5: AWS Free Tier Guardrails & Cost Protection](#phase-5-aws-free-tier-guardrails--cost-protection)
9. [Milestone Checklist for Hands-On Practice](#milestone-checklist)

---

## 1. Architecture Overview & Workflow

```
[ Developer ]
      │  (git push to GitHub)
      ▼
[ GitHub Actions (CI) ]
      ├── 1. Run unit / syntax tests
      ├── 2. Build Docker container image
      └── 3. Push Docker image to Container Registry (Docker Hub or AWS ECR)
      ▼
[ Terraform ] (IaC - Run once or on demand)
      └── Provisions AWS EC2 instance, VPC, Key Pair, and Security Groups (Ports 22, 5000, 80)
      ▼
[ Ansible / Deployment Job (CD) ]
      ├── Connects to EC2 instance via SSH
      ├── Configures system packages and installs Docker daemon
      ├── Pulls the newly built image from the Registry
      └── Stops old container & starts new container (Port 5000:5000)
      ▼
[ Live Application on AWS EC2 ]
```

---

## 2. Prerequisites & Local Tooling

Install the following tools on your local development machine:

| Tool | Purpose | Verification Command |
| :--- | :--- | :--- |
| **Git** | Source code version control | `git --version` |
| **Docker Desktop** | Building and running containers locally | `docker --version` |
| **AWS CLI v2** | Interacting with AWS account from CLI | `aws --version` |
| **Terraform CLI** | Provisioning AWS infrastructure declaratively | `terraform --version` |
| **Ansible** | Automating server configuration (WSL / Linux / MacOS) | `ansible --version` |
| **VS Code / Cursor** | Code editor with Docker, Terraform & YAML extensions | — |

### AWS Free Tier Account Setup Checklist
- [ ] Create an **AWS IAM User** (never use root user credentials for CLI/CI-CD).
- [ ] Attach permission policy: `AmazonEC2FullAccess` (and `AmazonECR` if using AWS ECR).
- [ ] Generate an **Access Key ID** and **Secret Access Key** for your IAM user.
- [ ] Configure local CLI credentials: `aws configure`.
- [ ] Set up a **Zero-Spend / $1 Budget Alert** in AWS Billing Console.

---

## 3. Recommended Repository Structure

Plan to organize your repository as follows as you build each phase:

```text
BE_PROJECT_GC14/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions CI/CD Pipeline definition
├── terraform/
│   ├── main.tf                     # EC2, Security Groups, Key Pair definitions
│   ├── variables.tf                # Input variables (region, instance type, etc.)
│   ├── outputs.tf                  # Outputs (Public IP, Instance ID)
│   └── terraform.tfvars.example    # Variable values template (do NOT commit secrets)
├── ansible/
│   ├── inventory.ini               # Dynamic/Static server IP target
│   └── playbook.yml                # Docker installation and container run tasks
├── model/
│   └── rf_model                    # Machine learning model artifact
├── templates/                      # Flask HTML templates
├── static/                         # CSS, JS, Images
├── app.py                          # Flask application entry point
├── config.json                     # Application configuration
├── crime.sql                       # Database schema
├── data.csv                        # Dataset for ML training
├── Dockerfile                      # Application Docker container recipe
├── .dockerignore                   # Exclude venv, .git, caches from Docker build
├── docker-compose.yml              # Local multi-container setup (Flask + MySQL)
├── requirements.txt                # Lean production dependencies
└── CICD_PIPELINE_GUIDE.md          # This reference guide
```

---

## Phase 1: Containerization with Docker

### Objective
Package the Python 3.11 web app, ML dependencies, and model into a self-contained image that runs identically on any environment.

### Core Concepts to Learn
- **Dockerfile instructions:** `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`.
- **Image Layer Caching:** Ordering steps so `requirements.txt` is installed before copying source code to speed up rebuilds.
- **Docker Compose:** Managing multiple related containers (e.g. Flask Web App + MySQL Database) on the same bridge network.
- **Environment Variables:** Passing database credentials into the container without hardcoding secrets in images.

### Hands-on Tasks
1. Create `.dockerignore` to ignore `venv/`, `__pycache__/`, `.git/`, and `.idea/`.
2. Create a clean, production-oriented `Dockerfile` using `python:3.11-slim`.
3. Build and test your Docker image locally:
   - Command: `docker build -t crime-prediction-app:latest .`
   - Command: `docker run -d -p 5000:5000 --name crime-app crime-prediction-app:latest`
4. Create a `docker-compose.yml` to spin up both the Flask app and a MySQL container with database initialization via `crime.sql`.

---

## Phase 2: Infrastructure as Code (IaC) with Terraform

### Objective
Define the cloud infrastructure on AWS programmatically so it can be created, updated, or destroyed in minutes.

### Core Concepts to Learn
- **Providers:** How Terraform talks to the AWS API (`hashicorp/aws`).
- **Resource Blocks:**
  - `aws_security_group`: Firewall rules allowing inbound Port 22 (SSH), Port 80 (HTTP), and Port 5000 (Flask).
  - `aws_key_pair`: Public key for SSH access.
  - `aws_instance`: Free-tier eligible compute instance (`t2.micro` or `t3.micro` running Ubuntu 22.04 LTS).
- **Terraform State (`terraform.tfstate`):** The single source of truth mapping your code to real AWS resources.

### Hands-on Tasks
1. Write `terraform/main.tf` with the AWS provider and region (`ap-south-1` or `us-east-1`).
2. Define the EC2 security group with:
   - Inbound: Port 22 (SSH), Port 5000 (App), Port 80 (HTTP).
   - Outbound: All traffic (`0.0.0.0/0`).
3. Define the EC2 resource using an Ubuntu AMI and instance type `t2.micro`.
4. Run Terraform lifecycle commands:
   - `terraform init` : Initialize the directory and download AWS provider.
   - `terraform plan` : Review the proposed changes before creation.
   - `terraform apply` : Deploy the actual server on AWS.
   - `terraform destroy` : Clean up resources when done to avoid AWS costs.

---

## Phase 3: Configuration Management with Ansible

### Objective
Automate post-provisioning configuration of the EC2 instance without manual SSH commands.

### Core Concepts to Learn
- **Agentless Architecture:** Ansible operates purely over SSH with Python installed on the target machine.
- **Inventory File (`inventory.ini`):** A list of target host IPs, usernames, and SSH key paths.
- **Playbooks (`playbook.yml`):** YAML files detailing the state you want to achieve on the server.
- **Idempotency:** Running a playbook multiple times will only apply changes if the server has drifted from the desired state.

### Hands-on Tasks
1. Write an `ansible/inventory.ini` pointing to the public IP of the EC2 instance created by Terraform.
2. Test SSH connectivity with Ansible Ping:
   - Command: `ansible all -i inventory.ini -m ping`
3. Write `ansible/playbook.yml` with tasks to:
   - Update `apt` cache and upgrade packages.
   - Install prerequisite packages (`apt-transport-https`, `ca-certificates`, `curl`).
   - Install the official Docker engine (`docker.io` or Docker CE).
   - Add the default `ubuntu` user to the `docker` group.
   - Ensure the Docker service is enabled and running.
   - Pull the application Docker image and run it on port `5000:5000`.
4. Execute the playbook:
   - Command: `ansible-playbook -i inventory.ini playbook.yml`

---

## Phase 4: CI/CD Automation with GitHub Actions

### Objective
Create an automated pipeline that tests, builds, and deploys the latest version of the application whenever code is pushed to GitHub.

### Core Concepts to Learn
- **Workflow Triggers:** `on: push: branches: [ main ]`
- **GitHub Hosted Runners:** Ubuntu virtual machines (`ubuntu-latest`) running your workflow steps.
- **GitHub Secrets:** Secure storage for sensitive values:
  - `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` (or AWS credentials for ECR).
  - `EC2_HOST` (Public IP of your EC2 server).
  - `EC2_SSH_KEY` (Private `.pem` key content).
  - `EC2_USER` (`ubuntu`).
- **Pipeline Stages:**
  - **Stage 1 (Continuous Integration - CI):** Checkout code $\rightarrow$ Run tests $\rightarrow$ Docker build $\rightarrow$ Push to Docker Hub / ECR.
  - **Stage 2 (Continuous Deployment - CD):** SSH into EC2 $\rightarrow$ Pull latest image $\rightarrow$ Stop running container $\rightarrow$ Start new container.

### Hands-on Tasks
1. Create `.github/workflows/deploy.yml`.
2. Add necessary repository secrets in GitHub (`Settings -> Secrets and variables -> Actions`).
3. Push a small commit (e.g., updating a template) to `main`.
4. Watch the GitHub Actions tab execute each step green.
5. Verify your change is live by opening `http://<EC2-PUBLIC-IP>:5000` in your web browser.

---

## Phase 5: AWS Free Tier Guardrails & Cost Protection

| Area | Best Practice | Risk Avoidance |
| :--- | :--- | :--- |
| **Compute** | Use `t2.micro` or `t3.micro` only. | Larger instances exceed 750 free hours/month limit. |
| **Storage** | Allocate 8 GB to 20 GB gp2/gp3 EBS volume. | Free tier covers up to 30 GB EBS total. |
| **Elastic IP** | Avoid allocating unused Elastic IPs. | AWS charges for Elastic IPs that are allocated but not attached to a running instance. |
| **Tear Down** | Run `terraform destroy` when not actively practicing. | Stops EC2 hours from accumulating when you step away for days. |
| **Secrets** | Never commit `.pem` keys, passwords, or AWS secrets to Git. | Add `*.pem`, `*.tfstate`, `*.tfstate.backup`, `.env` to `.gitignore`. |

---

## Milestone Checklist

Track your hands-on progress:

- [ ] **Milestone 1:** Create `Dockerfile` and run app successfully on local Docker.
- [ ] **Milestone 2:** Configure AWS CLI and verify Free Tier access via terminal.
- [ ] **Milestone 3:** Write Terraform files, run `terraform apply`, and verify EC2 is live in AWS Console.
- [ ] **Milestone 4:** SSH into the EC2 instance using your generated key pair.
- [ ] **Milestone 5:** Write Ansible playbook to install Docker on EC2 and verify with `ansible-playbook`.
- [ ] **Milestone 6:** Create Docker Hub / AWS ECR repository and push image manually.
- [ ] **Milestone 7:** Write `.github/workflows/deploy.yml` with secrets configured.
- [ ] **Milestone 8:** Push a commit to GitHub and watch automated zero-touch deployment succeed!
- [ ] **Milestone 9:** Practice running `terraform destroy` to prove reproducible infrastructure.
