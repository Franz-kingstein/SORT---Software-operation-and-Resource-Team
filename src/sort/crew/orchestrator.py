from .agents.agent_wrappers import MistralAgent, QwenAgent, LlamaAgent

# CrewAI and LangChain integrations
from crewai import Agent, Task, Crew, Process
from langchain.memory import ConversationBufferMemory

# Simple Docker sandbox runner interface
import subprocess
import tempfile
import os
import textwrap

from .github.github_agent import GitHubAgent, RepoSpec
from .github.docker_agent import DockerAgent
from .deploy.netlify_agent import NetlifyAgent
from .agents.project_synthesizer import ProjectSynthesizer

class SandboxRunner:
    """Run generated code safely inside a Docker container with resource limits."""
    def __init__(self, image: str = "python:3.12-slim", timeout: int = 10):
        self.image = image
        self.timeout = timeout

    def run_python(self, code: str) -> tuple[int, str, str]:
        # Write code to a temp file
        with tempfile.TemporaryDirectory() as tmp:
            code_path = os.path.join(tmp, "main.py")
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(textwrap.dedent(code))
            # Execute within Docker with constraints
            cmd = [
                "docker", "run", "--rm",
                "--network", "none",             # no network
                "--cpus", "0.5",                 # limit CPU
                "--memory", "256m",              # limit memory
                "-v", f"{code_path}:/app/main.py:ro",
                "-w", "/app",
                self.image,
                "bash", "-lc", f"python -B -I -X faulthandler -W ignore main.py"
            ]
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
                return proc.returncode, proc.stdout, proc.stderr
            except subprocess.TimeoutExpired as e:
                return 124, "", f"Timeout after {self.timeout}s"
            except FileNotFoundError:
                return 127, "", "Docker not found. Please install Docker to use sandbox runner."

class CrewOrchestrator:
    def __init__(self):
        self.mistral = MistralAgent()
        self.qwen = QwenAgent()
        self.llama = LlamaAgent()

        # LangChain memory for conversation context
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

        # CrewAI agents (optional for routing/audit)
        self.planner = Agent(role="Planner", goal="Plan tasks for DevOps/coding automation", backstory="", allow_delegation=False)
        self.coder = Agent(role="Coder", goal="Generate correct, minimal code", backstory="", allow_delegation=False)
        self.verifier = Agent(role="Verifier", goal="Verify code correctness and safety", backstory="", allow_delegation=False)
        self.crew = Crew(agents=[self.planner, self.coder, self.verifier], tasks=[], process=Process.sequential)

        # Sandbox
        self.sandbox = SandboxRunner()

        # Integrations
        try:
            self.github = GitHubAgent()
        except Exception:
            self.github = None
        self.docker_agent = DockerAgent()
        self.netlify_agent = None  # will be instantiated when needed
        self.synth = ProjectSynthesizer()

    def detect_project_type(self, plan: str, user_prompt: str) -> str:
        text = f"{plan}\n{user_prompt}".lower()
        if "next.js" in text or "nextjs" in text:
            return "nextjs"
        if "react" in text:
            return "react"
        if "node.js" in text or "nodejs" in text:
            return "node"
        if "django" in text:
            return "django"
        if "flask" in text:
            return "flask"
        if "python" in text:
            return "python"
        return "python"  # default

    def run_pipeline(
        self,
        user_prompt: str,
        github_export: bool = False,
        repo_owner: str | None = None,
        repo_name: str | None = None,
        create_docker: bool = False,
        image_name: str | None = None,
        deploy_netlify: bool = False,
        netlify_build_cmd: str | None = None,
        netlify_publish_dir: str | None = None,
        netlify_token: str | None = None,
    ):
        # Memory: log user prompt
        self.memory.chat_memory.add_user_message(user_prompt)

        # Step 1: Plan using Mistral
        plan = self.mistral.plan(user_prompt)
        self.memory.chat_memory.add_ai_message(f"Plan: {plan}")
        print("[Mistral Plan]", plan)

        # Step 2: Code generation using Qwen
        code = self.qwen.generate_code(plan)
        self.memory.chat_memory.add_ai_message(f"Code draft length: {len(code)}")
        print("[Qwen Code]", code)

        # Step 3: Static verification using Llama
        verification_prompt = (
            "You are a strict code verifier. Analyze this code for syntax issues, security concerns, and logic errors. "
            "Respond with a concise verdict and list of issues if any.\n\n" + code
        )
        validation = self.llama.validate_code(verification_prompt)
        print("[Llama Validation]", validation)

        # Step 2.5: Project synthesis (multi-file when needed)
        project_type = self.detect_project_type(plan, user_prompt)
        files = self.synth.synthesize(plan=plan, primary_code=code, user_prompt=user_prompt, project_type=project_type)

        # Optional: sandbox execution (prefer main.py if present)
        exec_status = {"status": "skipped", "rc": None, "stdout": "", "stderr": ""}
        to_run = None
        if "main.py" in files:
            to_run = files["main.py"]
        elif any(p.endswith(".py") for p in files):
            # pick a deterministic python entry
            for p, c in files.items():
                if p.endswith(".py"):
                    to_run = c
                    break
        else:
            if "python" in plan.lower() or code.strip().startswith(("import", "def ", "print(")):
                to_run = code
        if to_run:
            rc, out, err = self.sandbox.run_python(to_run)
            exec_status = {"status": "done", "rc": rc, "stdout": out, "stderr": err}

        # Optional: export to GitHub (requires token)
        repo_url = None
        if github_export and self.github and repo_owner and repo_name:
            spec = RepoSpec(owner=repo_owner, name=repo_name)
            files_to_push = dict(files)
            files_to_push.setdefault("README.md", f"# {repo_name}\n\nGenerated by SORT agents\n\n## Plan\n\n{plan}\n\n## Validation\n\n{validation}\n")
            repo_url = self.github.push_project_snapshot(spec, files_to_push, project_type=project_type, with_requirements=True)

            # Optional Docker setup under the same repo
            if create_docker:
                self.docker_agent.setup_docker_pipeline(
                    self.github,
                    spec,
                    project_type=project_type,
                    image_name=image_name,
                )

            # Optional Netlify setup: add netlify.toml for GitHub-based deploys
            if deploy_netlify:
                if netlify_token:
                    self.netlify_agent = NetlifyAgent(netlify_token)
                else:
                    self.netlify_agent = NetlifyAgent()  # will read NETLIFY_AUTH_TOKEN from env
                build_cmd = netlify_build_cmd or "npm run build"
                publish_dir = netlify_publish_dir or "dist"
                self.netlify_agent.add_netlify_config(
                    self.github,
                    spec,
                    build_cmd=build_cmd,
                    publish_dir=publish_dir,
                    env=None,
                )

        return {
            "plan": plan,
            "code": code,
            "files": files,
            "validation": validation,
            "execution": exec_status,
            "repo_url": repo_url,
        }

if __name__ == "__main__":
    # Intentionally no test script
    pass
