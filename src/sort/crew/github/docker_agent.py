from typing import Optional
from .github_agent import RepoSpec

class DockerAgent:
    """Handles Dockerfile creation and Docker CI workflow in GitHub repos."""

    def add_dockerfile(self, github_agent, repo, project_type: str = "python"):
        if project_type == "python":
            dockerfile = (
                "FROM python:3.12-slim\n"
                "ENV PYTHONDONTWRITEBYTECODE=1 \\\n    PYTHONUNBUFFERED=1\n"
                "WORKDIR /app\n"
                "COPY . /app\n"
                "RUN python -m pip install --upgrade pip \\\n    && if [ -f requirements.txt ]; then pip install -r requirements.txt; \\\n    elif [ -f pyproject.toml ]; then pip install . || true; else echo \"No deps\"; fi\n"
                "CMD [\"python\", \"-B\", \"-I\", \"app/main.py\"]\n"
            )
        else:
            dockerfile = "FROM alpine:3.19\nCMD [\"echo\", \"Hello from container\"]\n"
        github_agent.commit_file(repo, "Dockerfile", dockerfile, "Add Dockerfile")

    def add_actions_docker(self, github_agent, repo, image_name: str, registry_owner: str):
        workflow_path = ".github/workflows/docker.yml"
        ghcr_image = f"ghcr.io/{registry_owner}/{image_name}"
        docker_yaml = f"""
name: Docker CI
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: {ghcr_image}:latest
"""
        github_agent.commit_file(repo, workflow_path, docker_yaml.strip() + "\n", "Add Docker build/push workflow")

    def setup_docker_pipeline(
        self,
        github_agent,
        spec: RepoSpec,
        project_type: str = "python",
        image_name: Optional[str] = None,
    ) -> str:
        repo = github_agent.ensure_repo(spec)
        # Ensure requirements.txt exists because Docker build relies on it
        github_agent.add_requirements(repo)
        # Add Dockerfile and Docker workflow
        img = image_name or spec.name.lower().replace("_", "-")
        self.add_dockerfile(github_agent, repo, project_type=project_type)
        self.add_actions_docker(github_agent, repo, image_name=img, registry_owner=spec.owner)
        return repo.html_url
