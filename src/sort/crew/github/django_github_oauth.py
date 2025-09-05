# Django GitHub OAuth utility for SORT
# Requires: social-auth-app-django (recommended), or use requests for manual flow

import os
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from requests_oauthlib import OAuth2Session

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID") or getattr(settings, "GITHUB_CLIENT_ID", None)
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET") or getattr(settings, "GITHUB_CLIENT_SECRET", None)
GITHUB_AUTH_BASE = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_USER = "https://api.github.com/user"
GITHUB_API_EMAILS = "https://api.github.com/user/emails"
GITHUB_SCOPE = ["repo", "workflow", "read:org"]

# Step 1: Redirect user to GitHub for authorization
def github_login(request):
    github = OAuth2Session(GITHUB_CLIENT_ID, scope=GITHUB_SCOPE, redirect_uri=request.build_absolute_uri(reverse("github_callback")))
    auth_url, state = github.authorization_url(GITHUB_AUTH_BASE)
    request.session["github_oauth_state"] = state
    return redirect(auth_url)

# Step 2: GitHub redirects back to this callback
def github_callback(request):
    github = OAuth2Session(GITHUB_CLIENT_ID, state=request.session["github_oauth_state"], redirect_uri=request.build_absolute_uri(reverse("github_callback")))
    token = github.fetch_token(
        GITHUB_TOKEN_URL,
        client_secret=GITHUB_CLIENT_SECRET,
        authorization_response=request.build_absolute_uri(),
    )
    # Save token in session or user profile
    request.session["github_token"] = token
    # Optionally fetch user info
    user_info = github.get(GITHUB_API_USER).json()
    request.session["github_user"] = user_info
    return redirect("/dashboard/")  # or wherever you want

# Usage in your Django view:
# from .github.django_github_oauth import github_login, github_callback
# Add to urls.py:
# path('github/login/', github_login, name='github_login')
# path('github/callback/', github_callback, name='github_callback')

# When running CrewAI pipeline, pass request.session['github_token']['access_token'] to GitHubAgent
