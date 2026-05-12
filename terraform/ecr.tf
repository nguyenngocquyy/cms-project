resource "aws_ecr_repository" "cms_backend" {
  name                 = "cms-backend-tf"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "cms_frontend" {
  name                 = "cms-frontend-tf"
  image_tag_mutability = "MUTABLE"
}
