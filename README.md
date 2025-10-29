# Coding Simulation Agentic Framework

This project uses CrewAI and Google Gemini to simulate coding: generate software, push to GitHub, and deploy to Render.

## Setup

1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GITHUB_TOKEN`: Your GitHub personal access token (with repo creation permissions)
   - `RENDER_TOKEN`: Your Render personal access token

## Run

Execute `python src/main.py` to run the agentic framework. It will generate a simple Flask app, create a GitHub repo, push the code, and deploy to Render.

## Note

This is a basic implementation. For production, handle errors, improve code generation, and add more features.
