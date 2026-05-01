# CMS 3-Tier on AWS EKS

## Overview
This project deploys a 3-tier CMS application on AWS using EKS, ECR, RDS, GitHub Actions, ALB Ingress, and ACM.

## Tech Stack
- Frontend: React
- Backend: FastAPI
- Database: PostgreSQL
- Container: Docker
- Orchestration: Amazon EKS
- Registry: Amazon ECR
- CI/CD: GitHub Actions
- Networking: ALB, ACM
- Security: Security Group, AWS Shield Standard

## Phase 1 Scope
- Frontend + Backend + Database
- Docker containerization
- Push images to ECR
- Deploy to EKS
- Expose application through ALB
- HTTPS with ACM

## Not in Phase 1
- Terraform
- Redis
- Kafka
- WAF
- Monitoring
