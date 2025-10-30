import sys
import os
from flask import Flask, jsonify, request
# Import CORS to handle cross-origin requests from the browser
from flask_cors import CORS 
import uuid
from dotenv import load_dotenv

# --- CrewAI Setup (Adapted from your original script) ---
# NOTE: Ensure your src/agents path is correct relative to where you run this.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from crewai import Task, Crew
# Attempt to import agents (This will fail if not run from the correct directory structure)
try:
    from src.agents.crew_agents import code_generator, github_agent, render_agent
except ImportError:
    # Placeholder classes if imports fail, to allow Flask to run
    print("WARNING: Could not import crew agents. Using placeholders.")
    class PlaceholderAgent:
        def __init__(self, name): self.name = name
    code_generator = PlaceholderAgent("Code Generator")
    github_agent = PlaceholderAgent("GitHub Agent")
    render_agent = PlaceholderAgent("Render Agent")


load_dotenv()

app = Flask(__name__)
# Initialize CORS to allow requests from the browser's file protocol
CORS(app) 

def initialize_and_run_crew():
    """Initializes and runs the CrewAI workflow."""
    # Generate a unique repo name inside the function scope
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
        context=[task_generate_code]
    )

    # Task 3: Deploy to Render
    task_render = Task(
        description="Deploy the GitHub repository to Render hosting platform. Use Render's static site hosting to deploy the web application. Provide the live URL and deployment status.",
        agent=render_agent,
        expected_output="Live URL and deployment confirmation",
        context=[task_github]
    )

    # Create the crew
    crew = Crew(
        agents=[code_generator, github_agent, render_agent],
        tasks=[task_generate_code, task_github, task_render],
        verbose=True
    )

    print("--- Crew Kickoff Initiated ---")
    # Run the crew
    result = crew.kickoff()
    print("--- Crew Kickoff Completed ---")

    return {
        "status": "success",
        "message": "Crew finished execution.",
        "repo_name": repo_name,
        "final_output": result
    }


@app.route('/api/kickoff', methods=['POST'])
def kickoff_endpoint():
    """API endpoint to start the CrewAI process."""
    try:
        # Start the crew execution
        result = initialize_and_run_crew()

        return jsonify(result), 200

    except Exception as e:
        # Log the full error to the server console
        print(f"An error occurred during crew execution: {e}", file=sys.stderr)
        return jsonify({
            "status": "error",
            "message": f"Failed to run the crew: {str(e)}",
            "detailed_error": str(e)
        }), 500

if __name__ == '__main__':
    # You must run this Python file first before opening the HTML file!
    print("Starting Flask server on http://127.0.0.1:5000")
    print("Run the crew by opening index.html and clicking the button.")
    # Run Flask server
    app.run(debug=True)
