# Architecture

## Main Flow
User -> ALB -> Ingress -> Frontend/Backend -> RDS PostgreSQL

## Components
- React frontend
- FastAPI backend
- PostgreSQL database on RDS
- Docker images in ECR
- EKS cluster for deployment
- GitHub Actions for CI/CD

## Security (Phase 1)
- Security Groups
- ACM certificate
- AWS Shield Standard
- Kubernetes Secrets
