import os
from typing import Any, Dict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import httpx
from dotenv import load_dotenv

# Import your orchestrator and GitHubAgent
try:
    from sort.crew.github.github_agent import GitHubAgent, RepoSpec
    from sort.crew.orchestrator import CrewOrchestrator
except Exception:
    # Fallback relative import if package layout differs
    from ..crew.github.github_agent import GitHubAgent, RepoSpec
    from ..crew.orchestrator import CrewOrchestrator

# Load env from multiple common locations
load_dotenv()  # current working directory
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
load_dotenv(dotenv_path=os.path.join(os.getcwd(), "sort", ".env"))

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
OAUTH_CALLBACK_URL = os.getenv("GITHUB_OAUTH_CALLBACK", "http://localhost:8000/github/callback/")
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-secret-change-me")

app = FastAPI(title="SORT Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/github/login/")
async def github_login(request: Request):
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Missing GITHUB_CLIENT_ID")
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": OAUTH_CALLBACK_URL,
        "scope": "repo workflow",
        "allow_signup": "true",
    }
    qs = "&".join(f"{k}={httpx.QueryParams({k:v})[k]}" for k, v in params.items())
    url = f"https://github.com/login/oauth/authorize?{qs}"
    return RedirectResponse(url)


@app.get("/github/callback/")
async def github_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    if not (GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET):
        raise HTTPException(status_code=500, detail="Missing GitHub OAuth envs")

    async with httpx.AsyncClient(headers={"Accept": "application/json"}) as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": OAUTH_CALLBACK_URL,
            },
        )
        token_resp.raise_for_status()
        data = token_resp.json()

    access_token = data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail=f"OAuth exchange failed: {data}")

    request.session["gh_token"] = access_token
    # Optionally fetch user login for UX
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"}) as client:
        u = await client.get("https://api.github.com/user")
        user = u.json() if u.status_code == 200 else {}
    request.session["gh_login"] = user.get("login")

    # Back to frontend
    return RedirectResponse("http://localhost:5173/")


@app.post("/api/run-pipeline/")
async def run_pipeline(request: Request):
    body: Dict[str, Any] = await request.json()
    token = request.session.get("gh_token")
    if body.get("github_export") and not token:
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")

    prompt: str = body.get("prompt", "")
    repo_owner: str = body.get("repo_owner") or request.session.get("gh_login") or ""
    repo_name: str = body.get("repo_name") or "sort-generated-repo"
    create_docker: bool = body.get("create_docker", False)
    image_name: str = body.get("image_name")
    deploy_netlify: bool = body.get("deploy_netlify", False)
    netlify_build_cmd: str = body.get("netlify_build_cmd")
    netlify_publish_dir: str = body.get("netlify_publish_dir")
    # Optionally: netlify_token from session or env

    orchestrator = CrewOrchestrator()
    # Patch orchestrator's github agent to use user token if exporting
    if body.get("github_export") and token:
        orchestrator.github = GitHubAgent(oauth_token=token)

    result = orchestrator.run_pipeline(
        user_prompt=prompt,
        github_export=body.get("github_export", False),
        repo_owner=repo_owner,
        repo_name=repo_name,
        create_docker=create_docker,
        image_name=image_name,
        deploy_netlify=deploy_netlify,
        netlify_build_cmd=netlify_build_cmd,
        netlify_publish_dir=netlify_publish_dir,
        netlify_token=None,
    )
    return JSONResponse(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sort.backend.app:app", host="0.0.0.0", port=8000, reload=True)
