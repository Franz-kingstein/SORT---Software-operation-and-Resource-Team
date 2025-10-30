import sys
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path (so `src` is importable)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from crewai import Task, Crew
from src.agents.crew_agents import code_generator, github_agent, render_agent


def run_pipeline(user_prompt: str) -> str:
    """
    Core S.O.R.T pipeline: Generate code → GitHub → Render.
    Accepts a user prompt and returns the final deployment result.
    """
    repo_name = f"coding-sim-flask-app-{uuid.uuid4().hex[:6]}"

    task_generate_code = Task(
        description=f"Generate Python code for {user_prompt}. "
                    "The app must be a valid Flask application with a single route '/' that returns a proper HTML response.",
        agent=code_generator,
        expected_output="The complete, runnable Python code for the Flask app as a single string."
    )

    task_github = Task(
        description=f"Create a new public GitHub repository named '{repo_name}'. "
                    "Then, initialize a Git repo, commit the Flask code from the previous task, and push it to GitHub.",
        agent=github_agent,
        expected_output="The full HTTPS URL of the newly created GitHub repository.",
        context=[task_generate_code]
    )

    task_render = Task(
        description="Deploy the GitHub repository to Render as a Web Service (not static site, since it's a Flask app). "
                    "Use Render's auto-deploy from the main branch. Return the live public URL and confirm successful deployment.",
        agent=render_agent,
        expected_output="A string containing the live deployment URL and a confirmation that the app is running.",
        context=[task_github]
    )

    crew = Crew(
        agents=[code_generator, github_agent, render_agent],
        tasks=[task_generate_code, task_github, task_render],
        verbose=True
    )

    result = crew.kickoff()
    return str(result)


def main():
    """CLI entry point."""
    print("Describe the Flask app you'd like to build (e.g., 'a simple Flask app that shows Hello, World!'):")
    user_prompt = input("> ").strip()
    if not user_prompt:
        user_prompt = "a simple Flask web app that displays 'Hello, World!' on the homepage."

    try:
        result = run_pipeline(user_prompt)
        print("\n✅ Final Result:")
        print(result)
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()