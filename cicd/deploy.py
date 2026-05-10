import os
import subprocess
import sys


AWS_REGION = "ap-southeast-1"
AWS_ACCOUNT_ID = "919664459382"

BACKEND_IMAGE = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/cms-backend:latest"
FRONTEND_IMAGE = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/cms-frontend:latest"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")


def run(cmd, cwd=None):
    print("\n>>> RUN: {}".format(cmd))
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print("Command failed with exit code {}: {}".format(result.returncode, cmd))
        sys.exit(result.returncode)


def main():
    print("=== CI/CD DEPLOY START ===")
    print("PROJECT_ROOT =", PROJECT_ROOT)
    print("BACKEND_DIR =", BACKEND_DIR)
    print("FRONTEND_DIR =", FRONTEND_DIR)

    run(
        "aws ecr get-login-password --region {} | docker login --username AWS --password-stdin {}.dkr.ecr.{}.amazonaws.com".format(
            AWS_REGION, AWS_ACCOUNT_ID, AWS_REGION
        )
    )

    print("=== Build backend image ===")
    run("docker build -t cms-backend:latest .", cwd=BACKEND_DIR)
    run("docker tag cms-backend:latest {}".format(BACKEND_IMAGE))

    print("=== Build frontend image ===")
    run("docker build -t cms-frontend:latest .", cwd=FRONTEND_DIR)
    run("docker tag cms-frontend:latest {}".format(FRONTEND_IMAGE))

    print("=== Push backend image ===")
    run("docker push {}".format(BACKEND_IMAGE))

    print("=== Push frontend image ===")
    run("docker push {}".format(FRONTEND_IMAGE))

    print("=== Restart EKS deployments ===")
    run("kubectl rollout restart deployment cms-backend -n cms")
    run("kubectl rollout restart deployment cms-frontend -n cms")

    print("=== Wait for rollout ===")
    run("kubectl rollout status deployment cms-backend -n cms --timeout=300s")
    run("kubectl rollout status deployment cms-frontend -n cms --timeout=300s")

    print("=== CI/CD DEPLOY DONE ===")


if __name__ == "__main__":
    main()
