import os
from dataclasses import dataclass
from typing import Optional

from github import Github
from dotenv import load_dotenv

from ..utils.requirements import default_requirements

load_dotenv()

@dataclass
class RepoSpec:
    owner: str
    name: str
    private: bool = True
    description: str = "Repo managed by SORT agents"
    default_branch: str = "main"

class GitHubAgent:
    """Handles GitHub OAuth token usage, repo creation, file commits, CI setup, and requirements."""

    def __init__(self, oauth_token: Optional[str] = None):
        token = oauth_token or os.getenv("GITHUB_TOKEN")
        # Make client optional; allow dynamic per-call tokens
        self.gh = Github(token) if token else None

    def set_token(self, oauth_token: str):
        """Set or update the OAuth token on this agent instance."""
        self.gh = Github(oauth_token)

    def _require_client(self, oauth_token: Optional[str] = None) -> Github:
        """Return a Github client, preferring the provided token, then instance client, then env."""
        if oauth_token:
            return Github(oauth_token)
        if self.gh is not None:
            return self.gh
        env_token = os.getenv("GITHUB_TOKEN")
        if env_token:
            return Github(env_token)
        raise ValueError("Missing GitHub token. Provide oauth_token, call set_token(), or set GITHUB_TOKEN in env.")

    def ensure_repo(self, spec: RepoSpec, oauth_token: Optional[str] = None):
        gh = self._require_client(oauth_token)
        user = gh.get_user()
        # If owner differs and you have org access, adjust to get_organization
        if spec.owner and spec.owner != user.login:
            org = gh.get_organization(spec.owner)
            try:
                repo = org.get_repo(spec.name)
            except Exception:
                repo = org.create_repo(
                    name=spec.name,
                    private=spec.private,
                    description=spec.description,
                    auto_init=True,
                )
        else:
            try:
                repo = user.get_repo(spec.name)
            except Exception:
                repo = user.create_repo(
                    name=spec.name,
                    private=spec.private,
                    description=spec.description,
                    auto_init=True,
                )
        return repo

    def commit_file(self, repo, path: str, content: str, message: str, branch: str = "main"):
        try:
            existing = repo.get_contents(path, ref=branch)
            repo.update_file(existing.path, message, content, existing.sha, branch=branch)
        except Exception:
            repo.create_file(path, message, content, branch=branch)

    def add_actions_ci(self, repo, project_type: str = "python"):
        workflow_path = ".github/workflows/ci.yml"
        if project_type == "python":
            ci_yaml = f"""
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; \
          elif [ -f pyproject.toml ]; then pip install .; else echo "No deps"; fi
      - name: Lint
        run: |
          pip install ruff
          ruff check . || true
      - name: Run tests
        run: |
          if [ -d tests ]; then pytest -q; else echo "No tests"; fi
"""
        else:
            ci_yaml = """name: CI\n"""
        self.commit_file(repo, workflow_path, ci_yaml.strip() + "\n", "Add CI workflow")

    def add_requirements(self, repo, content: Optional[str] = None):
        reqs = (content or default_requirements()).strip() + "\n"
        self.commit_file(repo, "requirements.txt", reqs, "Add requirements.txt")

    def push_project_snapshot(
        self,
        spec: RepoSpec,
        files: dict[str, str],
        project_type: str = "python",
        with_requirements: bool = True,
        requirements_content: Optional[str] = None,
        oauth_token: Optional[str] = None,
    ):
        repo = self.ensure_repo(spec, oauth_token=oauth_token)
        for rel_path, content in files.items():
            self.commit_file(repo, rel_path, content, f"Add {rel_path}")
        if with_requirements:
            self.add_requirements(repo, requirements_content)
        self.add_actions_ci(repo, project_type=project_type)
        return repo.html_url
