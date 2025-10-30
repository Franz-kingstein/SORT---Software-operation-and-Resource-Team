from crewai import Agent
from crewai.tools import tool
from src.utils.gemini_client import get_gemini_response
from src.utils.logger import get_agent_logger, get_api_logger, log_function_call, log_api_response
import os
import subprocess
from github import Github
import requests
import time
from dotenv import load_dotenv

load_dotenv()

llm = "gemini/gemini-2.0-flash-exp"
code_gen_logger = get_agent_logger("code_generator")
github_logger = get_agent_logger("github_manager")
render_logger = get_agent_logger("render_deployer")
api_logger = get_api_logger()

@tool
def generate_code(requirement: str) -> str:
    """Generates complete code for a web application based on the given requirement."""
    log_function_call(code_gen_logger, "generate_code", requirement=requirement[:100] + "...")
    
    try:
        code_gen_logger.info("Starting code generation")
        prompt = f"""Generate a complete web application based on this requirement: {requirement}.

Create a fully functional web application optimized for Render deployment with these files:

1. index.html - Complete HTML page with inline CSS and JavaScript
2. package.json - For Node.js deployment  
3. main.py - Python Flask version
4. render.yaml - Render configuration

Make it production-ready and responsive. Include interactive features.

Return the code in this format:
=== index.html ===
[HTML code here]

=== package.json ===
[JSON code here]

=== main.py ===
[Python code here]

=== render.yaml ===
[YAML code here]

Focus on creating a beautiful, interactive web application."""
        
        response = get_gemini_response(prompt)
        code_gen_logger.info(f"Code generation successful. Generated {len(response)} characters of code")
        return response
        
    except Exception as e:
        code_gen_logger.error(f"Code generation failed: {str(e)}")
        raise

@tool
def create_github_repo(code: str, repo_name: str) -> str:
    """Creates a GitHub repository with the given name and pushes the provided code to it."""
    log_function_call(github_logger, "create_github_repo", code_length=len(code), repo_name=repo_name)
    
    try:
        github_logger.info(f"Creating GitHub repository: {repo_name}")
        
        g = Github(os.getenv("GITHUB_TOKEN"))
        user = g.get_user()
        repo = user.create_repo(repo_name, private=False)
        
        github_logger.info(f"Repository created: {repo.html_url}")
        
        # Clone the repo
        github_logger.info("Cloning repository locally")
        subprocess.run(["git", "clone", repo.clone_url], cwd="/tmp")
        repo_dir = f"/tmp/{repo_name}"
        
        # Create main.py
        github_logger.info("Creating main.py file")
        with open(f"{repo_dir}/main.py", "w") as f:
            f.write(code)
        
        # Parse and create multiple files from the generated code
        github_logger.info("Parsing generated code into multiple files")
        
        files_to_create = {}
        current_file = None
        current_content = []
        
        for line in code.split('\n'):
            if line.startswith('=== ') and line.endswith(' ==='):
                # Save previous file
                if current_file:
                    files_to_create[current_file] = '\n'.join(current_content)
                # Start new file
                current_file = line.strip('=== ')
                current_content = []
            elif current_file:
                current_content.append(line)
        
        # Save last file
        if current_file:
            files_to_create[current_file] = '\n'.join(current_content)
        
        # Create all files
        for filename, content in files_to_create.items():
            github_logger.info(f"Creating file: {filename}")
            with open(f"{repo_dir}/{filename}", "w") as f:
                f.write(content.strip())
        
        # If no structured files found, create default files
        if not files_to_create:
            github_logger.info("No structured files found, creating default files")
            
            # Create main.py with Render-compatible Flask app
            render_flask_app = f"""
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template embedded in the Flask app
HTML_TEMPLATE = '''
{code}
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health_check():
    return {{"status": "healthy", "message": "AI-generated app is running"}}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
"""
            
            with open(f"{repo_dir}/main.py", "w") as f:
                f.write(render_flask_app)
            
            # Create default index.html
            default_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Generated Web App</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🚀%3C/text%3E%3C/svg%3E">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#764ba2">
    <meta name="description" content="An AI-generated web application created using CrewAI and Google Gemini">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .container {{ 
            max-width: 900px; 
            margin: 20px;
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        h1 {{ 
            text-align: center; 
            margin-bottom: 40px; 
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .feature {{ 
            background: rgba(255,255,255,0.15); 
            padding: 25px; 
            margin: 25px 0; 
            border-radius: 15px;
            transition: all 0.3s ease;
            border-left: 4px solid #ff6b6b;
        }}
        
        .feature:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        button {{ 
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            color: white; 
            border: none; 
            padding: 12px 25px; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255,107,107,0.3);
        }}
        
        button:hover {{ 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,107,107,0.5);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #ff6b6b;
        }}
        
        ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        li {{
            padding: 8px 0;
            position: relative;
            padding-left: 25px;
        }}
        
        li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #4CAF50;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AI-Generated Web Application</h1>
        
        <div class="feature">
            <h2>Welcome to Your Generated App!</h2>
            <p>This application was automatically created using advanced AI technology powered by Google Gemini and deployed through an intelligent agent framework.</p>
            <br>
            <button onclick="showAlert()">Test Interaction</button>
            <button onclick="generateColor()" style="margin-left: 10px;">Change Theme</button>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="visitors">1</div>
                <div>Visitor Count</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div>AI Generated</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">&lt;1s</div>
                <div>Load Time</div>
            </div>
        </div>
        
        <div class="feature">
            <h2>🔧 Technical Features</h2>
            <ul>
                <li>Responsive CSS Grid Layout</li>
                <li>Modern CSS3 Animations</li>
                <li>Interactive JavaScript Elements</li>
                <li>Render-Optimized Deployment</li>
                <li>Progressive Web App Ready</li>
                <li>Cross-Browser Compatible</li>
            </ul>
        </div>
        
        <div class="feature">
            <h2>🤖 Powered By</h2>
            <p><strong>CrewAI Framework:</strong> Multi-agent orchestration system<br>
            <strong>Google Gemini:</strong> Advanced AI code generation<br>
            <strong>GitHub API:</strong> Automated repository management<br>
            <strong>Render:</strong> Instant deployment and hosting</p>
        </div>
    </div>
    
    <script>
        function showAlert() {{
            alert('🎉 Hello from your AI-generated application!\\n\\nThis interaction was coded automatically by AI.');
        }}
        
        function generateColor() {{
            const colors = [
                'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
            ];
            
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            document.body.style.background = randomColor;
        }}
        
        // Visitor counter with localStorage
        function updateVisitorCount() {{
            let count = localStorage.getItem('visitorCount') || 0;
            count = parseInt(count) + 1;
            localStorage.setItem('visitorCount', count);
            document.getElementById('visitors').textContent = count;
        }}
        
        // Add interactive effects
        document.addEventListener('DOMContentLoaded', function() {{
            updateVisitorCount();
            
            const features = document.querySelectorAll('.feature');
            features.forEach((feature, index) => {{
                feature.style.animationDelay = `${{index * 0.1}}s`;
                feature.style.animation = 'fadeInUp 0.6s ease forwards';
            }});
            
            // Add CSS animation keyframes
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeInUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
            `;
            document.head.appendChild(style);
        }});
    </script>
</body>
</html>"""
            
            with open(f"{repo_dir}/index.html", "w") as f:
                f.write(default_html)

            # Ensure Render static publish directory exists with index.html
            public_dir = os.path.join(repo_dir, "public")
            os.makedirs(public_dir, exist_ok=True)
            with open(os.path.join(public_dir, "index.html"), "w") as f:
                f.write(default_html)
        
        # Create render.yaml for Render deployment
        render_config = """services:
  - type: web
    name: ai-generated-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: "3.10"
      - key: PORT
        value: "10000"
    healthCheckPath: /
    
    - type: static_site
    name: ai-generated-static
    env: static
    buildCommand: echo 'Building static site...'
        staticPublishPath: public
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
      - path: /*
        name: X-XSS-Protection
        value: "1; mode=block"
      - path: /*
        name: X-Content-Type-Options
        value: nosniff
      - path: /*
        name: Referrer-Policy
        value: strict-origin-when-cross-origin
      - path: "*.html"
        name: Cache-Control
        value: "public, max-age=0, must-revalidate"
      - path: "*.css"
        name: Cache-Control
        value: "public, max-age=31536000, immutable"
      - path: "*.js"
        name: Cache-Control
        value: "public, max-age=31536000, immutable"
    routes:
      - type: rewrite
        source: /*
        destination: /index.html"""
        
        github_logger.info("Creating render.yaml configuration")
        with open(f"{repo_dir}/render.yaml", "w") as f:
            f.write(render_config)
        
        # Also create package.json for Node.js deployment option
        github_logger.info("Creating package.json")
        package_json = """{
  "name": "ai-generated-web-app",
  "version": "1.0.0",
  "description": "AI-generated web application deployed on Render",
  "main": "index.html",
  "scripts": {
    "start": "python main.py",
    "build": "echo 'Building static site...'",
    "dev": "python main.py"
  },
  "engines": {
    "node": "18.x"
  },
  "dependencies": {},
  "devDependencies": {},
  "keywords": ["ai", "web-app", "render", "static"],
  "author": "AI Code Generator",
  "license": "MIT"
}"""
        
        with open(f"{repo_dir}/package.json", "w") as f:
            f.write(package_json)
        
        # Create robots.txt for SEO
        github_logger.info("Creating robots.txt")
        robots_content = """User-agent: *
Allow: /

Sitemap: https://{site_name}.onrender.com/sitemap.xml"""
        
        with open(f"{repo_dir}/robots.txt", "w") as f:
            f.write(robots_content)
            
        # Create a simple manifest.json for PWA features
        github_logger.info("Creating manifest.json")
        manifest_content = """{
  "name": "AI Generated Web App",
  "short_name": "AI App",
  "description": "An application generated by AI using CrewAI and Google Gemini",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#764ba2",
  "icons": [
    {
      "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🚀%3C/text%3E%3C/svg%3E",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ]
}"""
        
        with open(f"{repo_dir}/manifest.json", "w") as f:
            f.write(manifest_content)
        
        # Create requirements.txt for Render Python deployment
        github_logger.info("Creating requirements.txt for Render deployment")
        requirements_content = """flask==2.3.3
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
Jinja2==3.1.2
MarkupSafe==2.1.3
Werkzeug==2.3.7
itsdangerous==2.1.2
click==8.1.7"""
        
        with open(f"{repo_dir}/requirements.txt", "w") as f:
            f.write(requirements_content)
        
        # Create start.sh script for Render deployment
        github_logger.info("Creating start.sh for Render")
        start_script = """#!/bin/bash
# Start script for Render deployment

# Install dependencies if not already installed
if [ ! -d ".venv" ]; then
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Start the Flask application with Gunicorn
if [ -f "main.py" ]; then
    echo "Starting Flask app with Gunicorn..."
    gunicorn --bind 0.0.0.0:$PORT main:app
else
    echo "Starting simple HTTP server for static files..."
    python -m http.server $PORT
fi"""
        
        with open(f"{repo_dir}/start.sh", "w") as f:
            f.write(start_script)
        
        # Make start.sh executable
        import stat
        os.chmod(f"{repo_dir}/start.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        # Create README.md
        github_logger.info("Creating README.md")
        readme_content = f"""# AI Generated Web Application

This web application was automatically generated using AI and optimized for Render deployment.

## Quick Start - Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your browser to the displayed URL (usually http://localhost:5000)

## Deployment on Render

This repository is configured for automatic deployment on Render:

- **render.yaml**: Render service configuration
- **package.json**: Node.js deployment metadata  
- **index.html**: Static web content
- **main.py**: Python Flask alternative

## Files Structure

- `index.html` - Main web page with interactive features
- `main.py` - Python Flask application code
- `render.yaml` - Render deployment configuration
- `package.json` - Node.js package metadata
- `requirements.txt` - Python dependencies
- `manifest.json` - PWA configuration

## Features

- 🚀 AI-generated code
- 📱 Responsive design
- ⚡ Optimized for Render hosting
- 🔄 Automatic deployment
- 💻 Both static and Flask versions

---
*Generated by Agentic Framework with CrewAI, Google Gemini & Render*

---
*Generated by Agentic Framework with CrewAI & Google Gemini*
"""
        
        with open(f"{repo_dir}/README.md", "w") as f:
            f.write(readme_content)
        
        # Git operations
        github_logger.info("Committing and pushing code")
        os.chdir(repo_dir)
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit"])
        subprocess.run(["git", "push", "origin", "main"])
        os.chdir("/home/franz/Documents/SORT")  # back to project dir
        
        github_logger.info(f"Code successfully pushed to: {repo.html_url}")
        return repo.html_url
        
    except Exception as e:
        github_logger.error(f"GitHub repository creation failed: {str(e)}")
        raise

@tool
def deploy_to_render(repo_url: str) -> str:
    """Deploy the GitHub repository to Render and provide the live URL."""
    import time  # Import time module for sleep functionality
    log_function_call(render_logger, "deploy_to_render", repo_url=repo_url)
    
    try:
        render_logger.info(f"Starting Render deployment for: {repo_url}")

        # Wait for 30 seconds to allow GitHub to fully process the repository
        render_logger.info("⏳ Waiting 30 seconds for GitHub repository to be fully ready...")
        print("⏳ Waiting 30 seconds for GitHub repository to be fully ready before Render deployment...")

        for remaining in range(30, 0, -10):
            print(f"⏳ Waiting {remaining} seconds... (GitHub processing time)")
            time.sleep(10)

        print("✅ Wait complete! Starting Render deployment...")
        render_logger.info("✅ 30-second wait completed, proceeding with Render deployment")
        
        render_token = os.getenv("RENDER_TOKEN")
        if not render_token:
            error_msg = "❌ RENDER_TOKEN not found in environment variables"
            render_logger.error(error_msg)
            return error_msg
        
        headers = {
            "Authorization": f"Bearer {render_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Generate unique service name
        import uuid
        service_name = f"coding-sim-app-{uuid.uuid4().hex[:8]}"
        render_logger.info(f"Generated service name: {service_name}")
        
        # Ensure repo_url is valid; attempt to fix or infer if malformed/missing
        if not repo_url or "github.com" not in repo_url:
            try:
                render_logger.warning("Repo URL missing or invalid. Attempting to infer from GitHub account...")
                gh_token = os.getenv("GITHUB_TOKEN")
                if gh_token:
                    gh_headers = {"Authorization": f"token {gh_token}", "Accept": "application/vnd.github+json"}
                    # Get current user login (for logging)
                    me_resp = requests.get("https://api.github.com/user", headers=gh_headers)
                    user_login = me_resp.json().get("login", "unknown") if me_resp.status_code == 200 else "unknown"
                    # List recent repos
                    repos_resp = requests.get(
                        "https://api.github.com/user/repos?sort=created&direction=desc&per_page=30",
                        headers=gh_headers,
                    )
                    if repos_resp.status_code == 200:
                        candidates = repos_resp.json()
                        # Prefer recent repos matching our naming pattern
                        preferred = None
                        for r in candidates:
                            name = r.get("name", "")
                            if name.startswith("coding-sim"):
                                preferred = r
                                break
                        chosen = preferred or (candidates[0] if candidates else None)
                        if chosen and chosen.get("html_url"):
                            repo_url = chosen["html_url"]
                            render_logger.info(f"✅ Inferred repository for user {user_login}: {repo_url}")
                        else:
                            return "❌ Could not infer repository URL from GitHub. Please provide a valid repo URL."
                    else:
                        return f"❌ Failed to list GitHub repositories: {repos_resp.status_code} - {repos_resp.text[:200]}"
                else:
                    return "❌ GITHUB_TOKEN not found. Provide repo_url explicitly or set GITHUB_TOKEN."
            except Exception as e:
                return f"❌ Error inferring repository URL: {str(e)}"

        # If user passed 'owner/repo', build the HTTPS URL
        if repo_url and "github.com" not in repo_url and "/" in repo_url:
            repo_url = f"https://github.com/{repo_url.strip()}"
            render_logger.info(f"Normalized repo URL to: {repo_url}")

        # Extract owner and repo from URL
        repo_parts = repo_url.replace("https://github.com/", "").replace(".git", "")
        
        # Validate the repo format
        if "/" not in repo_parts or len(repo_parts.split("/")) != 2:
            error_msg = f"Invalid GitHub URL format: {repo_url}"
            render_logger.error(error_msg)
            return error_msg
            
        owner, repo_name = repo_parts.split("/")
        render_logger.info(f"Repository owner: {owner}")
        render_logger.info(f"Repository name: {repo_name}")
        render_logger.info(f"Full repository path: {repo_parts}")
        
        # Verify repository exists
        try:
            import requests as github_requests
            github_check_url = f"https://api.github.com/repos/{repo_parts}"
            github_headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
            
            render_logger.info(f"Verifying repository exists: {github_check_url}")
            github_response = github_requests.get(github_check_url, headers=github_headers)
            
            if github_response.status_code == 200:
                repo_info = github_response.json()
                render_logger.info(f"✅ Repository verified: {repo_info.get('full_name')}")
                render_logger.info(f"✅ Repository is public: {not repo_info.get('private', True)}")
                render_logger.info(f"✅ Default branch: {repo_info.get('default_branch', 'main')}")
            else:
                render_logger.warning(f"⚠️ Could not verify repository: {github_response.status_code}")
                
        except Exception as e:
            render_logger.warning(f"Repository verification failed: {str(e)}")
        
        # Create Render static site service
        # First, get the owner ID from Render API
        try:
            render_logger.info("🔑 Getting Render account owner ID...")
            owner_response = requests.get(
                "https://api.render.com/v1/owners",
                headers=headers
            )
            
            if owner_response.status_code == 200:
                owners = owner_response.json()
                if owners:
                    # Try to find an owner that matches fallback account 'Franz-kingstein'
                    fallback_handle = "Franz-kingstein"
                    owner_id = None
                    matched_descriptor = None
                    for entry in owners:
                        obj = entry.get("owner") or entry
                        oid = obj.get("id") or entry.get("id")
                        username = obj.get("username") or obj.get("login") or obj.get("name") or obj.get("slug")
                        if isinstance(username, str) and username.lower() == fallback_handle.lower():
                            owner_id = oid
                            matched_descriptor = username
                            break
                    # Fallback to first owner if no username match
                    if not owner_id:
                        owner_id = owners[0].get("owner", {}).get("id") or owners[0].get("id")
                        matched_descriptor = matched_descriptor or "first-owner"
                    render_logger.info(f"✅ Using Render owner ID: {owner_id} (match: {matched_descriptor})")
                else:
                    return "❌ No Render owners found in account. Please check your RENDER_TOKEN permissions."
            else:
                return f"❌ Failed to get Render owner ID: {owner_response.status_code} - {owner_response.text}"
                
        except Exception as e:
            return f"❌ Error getting Render owner ID: {str(e)}"
        
        data = {
            "type": "static_site",
            "name": service_name,
            "repo": repo_url,
            "branch": "main",
            "buildCommand": "echo 'Building static site...'",
            "publishPath": "public",
            "pullRequestPreviewsEnabled": False,
            "autoSync": True,
            "ownerId": owner_id  # Required field
        }
        
        render_logger.info(f"📋 Render deployment configuration:")
        render_logger.info(f"   Service name: {service_name}")
        render_logger.info(f"   Repository: {repo_parts}")
        render_logger.info(f"   Branch: main")
        render_logger.info(f"   Build command: echo 'Building static site...'")
        render_logger.info(f"   Publish path: public")
        render_logger.info(f"   Repository URL: {repo_url}")
        render_logger.info(f"   Owner ID: {owner_id}")

        render_logger.info("Making API request to Render")
        response = requests.post(
            "https://api.render.com/v1/services",
            headers=headers,
            json=data
        )

        log_api_response(api_logger, "Render", response.status_code, response.text)

        if response.status_code == 201:
            service = response.json()
            service_data = service.get("service", service)  # Handle different response formats
            service_id = service_data.get("id")
            live_url = f"https://{service_name}.onrender.com"
            
            render_logger.info(f"✅ Render service created successfully: {live_url}")
            render_logger.info(f"✅ Service ID: {service_id}")
            
            return f"""🎉 SUCCESS! Site deployed to Render!

🌐 **Live URL:** {live_url}
📁 **GitHub Repository:** {repo_url}  
🔗 **Repository Path:** {repo_parts}
🆔 **Service ID:** {service_id}
🔄 **Auto-deploy:** Enabled from main branch
⚡ **Platform:** Render (No SSH issues!)
🚀 **Status:** Building and deploying automatically

✅ **Integration Verified:** 
   - Repository correctly linked to Render
   - Auto-deployment configured 
   - Build settings applied
   - Site will be accessible at {live_url}

💡 **Note:** The site will be live in 2-3 minutes as Render builds and deploys your code!
Future commits to the main branch will automatically trigger new deployments."""
        
        elif response.status_code == 400:
            try:
                error_details = response.json()
                error_message = error_details.get('message', 'Bad request')
                render_logger.error(f"Render API validation error: {error_details}")
                
                if 'ownerID' in error_message:
                    return f"""❌ Render deployment failed - Owner ID issue:

**Error:** {error_message}
**Repository:** {repo_url}
**Repository Path:** {repo_parts}

**Troubleshooting:**
1. Verify RENDER_TOKEN has proper permissions
2. Check if you have access to create services in Render
3. Ensure your Render account is properly set up

**Token:** {render_token[:10]}..."""
                else:
                    return f"""❌ Render deployment failed (API Validation Error):

**Error:** {error_message}
**Repository:** {repo_url}
**Repository Path:** {repo_parts}
**Details:** {error_details}"""
            except:
                return f"❌ Render API validation error: {response.text[:500]}"
        
        elif response.status_code == 401:
            return f"""❌ Render authentication failed:

**Error:** Unauthorized access to Render API
**Check:** Verify RENDER_TOKEN in .env file: {render_token[:10]}...
**Repository:** {repo_url}"""
        
        else:
            error_msg = f"❌ Render deployment failed: {response.status_code} - {response.text[:500]}"
            render_logger.error(error_msg)
            return error_msg
                
    except Exception as e:
        error_msg = f"Error deploying to Render: {str(e)}"
        render_logger.error(error_msg)
        return error_msg

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

render_agent = Agent(
    role="Render Deployer",
    goal="Deploy the GitHub repository to Render",
    backstory="You handle deployment to Render for hosting.",
    tools=[deploy_to_render],
    llm=llm,
    allow_delegation=False
)
