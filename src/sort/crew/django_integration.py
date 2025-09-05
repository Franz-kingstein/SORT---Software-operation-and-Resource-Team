# Example: Django view to run CrewAI pipeline with dynamic GitHub token
# Place this in your Django app (e.g., views.py or a dedicated integration module)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .orchestrator import CrewOrchestrator
from .github.github_agent import RepoSpec
import json

@csrf_exempt
@login_required
def run_pipeline_with_github(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body)
    user_prompt = data.get("prompt")
    repo_name = data.get("repo_name")
    # Get GitHub token and user from session (set by OAuth)
    github_token = request.session.get("github_token", {}).get("access_token")
    github_user = request.session.get("github_user", {}).get("login")
    if not github_token or not github_user:
        return JsonResponse({"error": "GitHub not authenticated"}, status=401)
    # Run CrewAI pipeline with dynamic token
    orchestrator = CrewOrchestrator()
    orchestrator.github = orchestrator.github.__class__(oauth_token=github_token)  # Patch agent with user token
    result = orchestrator.run_pipeline(
        user_prompt,
        github_export=True,
        repo_owner=github_user,
        repo_name=repo_name,
    )
    return JsonResponse(result)

# Usage:
# Add to urls.py:
# path('api/run-pipeline/', run_pipeline_with_github, name='run_pipeline_with_github')
# POST JSON: {"prompt": "your task", "repo_name": "your-repo"}
# Requires user to be logged in and GitHub OAuth completed
