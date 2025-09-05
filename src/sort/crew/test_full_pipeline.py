"""
Test script for the full SORT pipeline: planning, codegen, review, sandbox, GitHub, Docker, and Netlify config.
- Only runs each API call once.
- Uses environment variables for all tokens and user info.
- Prints summary/results for manual inspection.
"""
import os
from src.sort.crew.orchestrator import CrewOrchestrator

# Load secrets from env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")  # GitHub username/org for repo owner
NETLIFY_AUTH_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")

# Test parameters
PROMPT = "Create a Python script that prints Fibonacci numbers up to 100."
REPO_NAME = os.getenv("TEST_REPO_NAME", "sort-pipeline-test-repo")
IMAGE_NAME = os.getenv("TEST_IMAGE_NAME", "sort-pipeline-test-image")

# Only run if all required tokens are present
if not (GITHUB_TOKEN and GITHUB_USER):
    print("Missing GITHUB_TOKEN or GITHUB_USER in environment. Skipping test.")
    exit(0)

# Instantiate orchestrator
orchestrator = CrewOrchestrator()

# Run pipeline with all options enabled (but only once)
result = orchestrator.run_pipeline(
    user_prompt=PROMPT,
    github_export=True,
    repo_owner=GITHUB_USER,
    repo_name=REPO_NAME,
    create_docker=True,
    image_name=IMAGE_NAME,
    deploy_netlify=bool(NETLIFY_AUTH_TOKEN),
    netlify_build_cmd="python main.py",  # or "npm run build" for frontend
    netlify_publish_dir=".",
    netlify_token=NETLIFY_AUTH_TOKEN,
)

print("\n--- SORT Pipeline Test Result ---")
for k, v in result.items():
    print(f"{k}:\n{v}\n")
