output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "backend_ecr_url" {
  value = aws_ecr_repository.cms_backend.repository_url
}

output "frontend_ecr_url" {
  value = aws_ecr_repository.cms_frontend.repository_url
}
