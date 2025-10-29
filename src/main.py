import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from crewai import Task, Crew
from src.agents.crew_agents import code_generator, github_agent, netlify_agent
import uuid
from dotenv import load_dotenv

load_dotenv()

# Generate a unique repo name
repo_name = f"coding-sim-flask-app-{uuid.uuid4().hex[:6]}"

# Task 1: Generate code
task_generate_code = Task(
    description="Generate Python code for a simple Flask web app that displays 'Hello, World!' on the homepage.",
    agent=code_generator,
    expected_output="The complete Python code for the app."
)

# Task 2: Create GitHub repo and push code
task_github = Task(
    description=f"Create a GitHub repository named '{repo_name}' and push the generated code to it.",
    agent=github_agent,
    expected_output="The URL of the created GitHub repository.",
    context=[task_generate_code]  # Access output from previous task
)

# Task 3: Deploy to Netlify
task_netlify = Task(
    description="Deploy the GitHub repository to Netlify using the repository URL provided in the context from the GitHub task, and provide the live URL.",
    agent=netlify_agent,
    expected_output="The live URL of the deployed service.",
    context=[task_github]
)

# Create the crew
crew = Crew(
    agents=[code_generator, github_agent, netlify_agent],
    tasks=[task_generate_code, task_github, task_netlify]
)

# Run the crew
if __name__ == "__main__":
    result = crew.kickoff()
    print("Final Result:", result)
