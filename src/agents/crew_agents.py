from crewai import Agent
from crewai.tools import tool
from src.utils.gemini_client import get_gemini_response
import os
import subprocess
from github import Github
import requests
from dotenv import load_dotenv

load_dotenv()

llm = "gemini/gemini-2.5-flash"

@tool
def generate_code(requirement: str) -> str:
    """Generates complete Python code for a simple application based on the given requirement."""
    prompt = f"Generate complete Python code for a simple application based on this requirement: {requirement}. Provide the code in a single file if possible."
    return get_gemini_response(prompt)

@tool
def create_github_repo(code: str, repo_name: str) -> str:
    """Creates a GitHub repository with the given name and pushes the provided code to it."""
    g = Github(os.getenv("GITHUB_TOKEN"))
    user = g.get_user()
    repo = user.create_repo(repo_name, private=False)
    
    # Clone the repo
    subprocess.run(["git", "clone", repo.clone_url], cwd="/tmp")  # clone to /tmp to avoid mess
    repo_dir = f"/tmp/{repo_name}"
    
    # Create main.py
    with open(f"{repo_dir}/main.py", "w") as f:
        f.write(code)
    
    # Git operations
    os.chdir(repo_dir)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    subprocess.run(["git", "push", "origin", "main"])
    os.chdir("/home/franz/Documents/SORT")  # back to project dir
    
    return repo.html_url

@tool
def deploy_to_netlify(repo_url: str) -> str:
    """Deploy the GitHub repository to Netlify and provide the live URL."""
    try:
        netlify_token = os.getenv("NETLIFY_TOKEN")
        headers = {"Authorization": f"Bearer {netlify_token}", "Content-Type": "application/json"}
        
        # Generate unique site name
        import uuid
        site_name = f"coding-sim-app-{uuid.uuid4().hex[:8]}"
        
        # Create site from repo
        data = {
            "name": site_name,
            "repo": {
                "provider": "github",
                "repo": repo_url.replace("https://github.com/", "").replace(".git", ""),
                "private": False,
                "branch": "main"
            }
        }
        response = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json=data)
        
        if response.status_code == 201:
            site = response.json()
            live_url = site.get("url", f"https://{site_name}.netlify.app")
            return f"Successfully deployed to Netlify! Live URL: {live_url}"
        else:
            return f"Error deploying to Netlify: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error deploying to Netlify: {str(e)}"

code_generator = Agent(
    role="Code Generator",
    goal="Generate software code based on user requirements",
    backstory="You are an expert coder who uses AI to generate high-quality code.",
    tools=[generate_code],
    llm=llm,
    allow_delegation=False
)

github_agent = Agent(
    role="GitHub Manager",
    goal="Create GitHub repository and push code",
    backstory="You manage GitHub repositories for code deployment.",
    tools=[create_github_repo],
    llm=llm,
    allow_delegation=False
)

netlify_agent = Agent(
    role="Netlify Deployer",
    goal="Deploy the GitHub repository to Netlify",
    backstory="You handle deployment to Netlify for hosting.",
    tools=[deploy_to_netlify],
    llm=llm,
    allow_delegation=False
)
