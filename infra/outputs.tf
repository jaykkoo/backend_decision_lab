# Infrastructure – Terraform

This directory provisions the production infrastructure using Terraform.

## Stack
- DigitalOcean Kubernetes (DOKS)
- Auto-scaled node pool
- DigitalOcean Container Registry
- GitHub Actions CI/CD compatible

## Components
- Kubernetes cluster with node autoscaling
- Docker registry for application images
- Infrastructure as Code (Terraform)

## Usage

```bash
terraform init
terraform plan
terraform apply
