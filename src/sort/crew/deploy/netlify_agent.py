import os
from typing import Optional

from ..github.github_agent import RepoSpec
from ..github.github_agent import GitHubAgent

NETLIFY_AUTH_URL = "https://app.netlify.com/authorize"
NETLIFY_API_BASE = "https://api.netlify.com/api/v1"

class NetlifyAgent:
    """Handles Netlify integration via GitHub: OAuth token handling (frontend), linking repo, and optional deploy config."""

    def __init__(self, netlify_token: Optional[str] = None):
        # In practice, obtain via Netlify OAuth (frontend flow), then pass to backend
        self.token = netlify_token or os.getenv("NETLIFY_AUTH_TOKEN")

    def netlify_headers(self):
        if not self.token:
            raise ValueError("Missing Netlify token. Provide netlify_token or set NETLIFY_AUTH_TOKEN in env.")
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def add_netlify_config(self, github_agent: GitHubAgent, spec: RepoSpec, build_cmd: str, publish_dir: str, env: Optional[dict] = None):
        repo = github_agent.ensure_repo(spec)
        netlify_toml = f"""
[build]
  command = "{build_cmd}"
  publish = "{publish_dir}"

# Example redirects, update as needed
# [[redirects]]
#   from = "/api/*"
#   to = "https://your-backend.example.com/:splat"
#   status = 200
"""
        github_agent.commit_file(repo, "netlify.toml", netlify_toml.strip() + "\n", "Add Netlify config")
        # Optionally add environment variables file
        if env:
            env_lines = "\n".join([f"{k}={v}" for k, v in env.items()]) + "\n"
            github_agent.commit_file(repo, "netlify.env.example", env_lines, "Add Netlify env example")
        return repo.html_url

    # Note: Full site creation/linking to GitHub via Netlify API requires a frontend OAuth flow to get token
    # and then calling Netlify API: POST /sites, with repo provider linked. That’s typically done outside Python backend.
