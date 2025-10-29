import streamlit as st
import subprocess
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup frontend logger
frontend_logger = setup_logger("streamlit_frontend", "frontend.log")

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(page_title="Coding Simulation Framework", layout="wide")

st.title("🤖 Coding Simulation Agentic Framework")
st.markdown("### Generate Software, Deploy to GitHub & Netlify Automatically")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    st.info("This framework uses CrewAI with Google Gemini to simulate coding: generate software, push to GitHub, and deploy to Netlify.")
    
    # Check if environment variables are set
    gemini_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    netlify_token = os.getenv("NETLIFY_TOKEN")
    
    st.subheader("Environment Status")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Gemini API:**")
        st.write("**GitHub Token:**")
        st.write("**Netlify Token:**")
    with col2:
        st.write("✅ Set" if gemini_key else "❌ Not Set")
        st.write("✅ Set" if github_token else "❌ Not Set")
        st.write("✅ Set" if netlify_token else "❌ Not Set")
    
    if not all([gemini_key, github_token, netlify_token]):
        st.warning("⚠️ Not all required tokens are set. Please configure .env file.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Project Generation")
    st.markdown("---")
    
    # Input section
    project_description = st.text_area(
        "Describe your application:",
        placeholder="e.g., Create a simple Flask web app that displays 'Hello, World!' on the homepage.",
        height=100
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        run_button = st.button("🚀 Generate & Deploy", use_container_width=True)
    
    with col_btn2:
        clear_button = st.button("🔄 Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.clear()
        st.rerun()

with col2:
    st.header("Quick Stats")
    st.markdown("---")
    st.metric("Generated Repos", "N/A", "Click Generate to start")
    st.metric("Deployed Sites", "N/A", "Real-time updates")
    st.metric("Success Rate", "N/A", "Tracking")

# Result section
st.markdown("---")

if run_button:
    if not project_description.strip():
        st.error("❌ Please describe your application first!")
        frontend_logger.warning("User attempted to run without project description")
    else:
        frontend_logger.info(f"Starting pipeline for project: {project_description[:100]}...")
        with st.spinner("🔄 Initializing CrewAI agents..."):
            st.info("Starting the agentic framework...")
            
            # Create a progress placeholder
            progress_placeholder = st.empty()
            result_placeholder = st.empty()
            
            try:
                # Run the main.py script and capture output
                process = subprocess.Popen(
                    [sys.executable, "src/main.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd="/home/franz/Documents/SORT"
                )
                
                stdout, stderr = process.communicate(timeout=300)
                
                if process.returncode == 0:
                    st.success("✅ Pipeline Completed Successfully!")
                    frontend_logger.info("Pipeline execution completed successfully")
                    
                    # Display output
                    with st.expander("📋 Full Output Log", expanded=True):
                        st.code(stdout, language="text")
                    
                    # Parse and display results
                    if "Final Result:" in stdout:
                        result_text = stdout.split("Final Result:")[-1].strip()
                        
                        if "Successfully deployed" in result_text and "netlify.app" in result_text:
                            st.success("🎉 Deployment Successful!")
                            frontend_logger.info("Deployment successful")
                            
                            # Extract and display URLs
                            lines = result_text.split("\n")
                            for line in lines:
                                if "https://" in line:
                                    st.write(f"**Live URL:** {line.strip()}")
                                    st.markdown(f"[🌐 Open in Browser]({line.strip()})", unsafe_allow_html=True)
                                    frontend_logger.info(f"Live URL generated: {line.strip()}")
                        else:
                            st.warning("⚠️ Pipeline ran but deployment may have issues.")
                            st.write(result_text)
                            frontend_logger.warning("Pipeline completed with issues")
                else:
                    st.error(f"❌ Pipeline Failed with Return Code: {process.returncode}")
                    frontend_logger.error(f"Pipeline failed with return code: {process.returncode}")
                    if stderr:
                        with st.expander("📋 Error Details", expanded=True):
                            st.code(stderr, language="text")
                        frontend_logger.error(f"Error details: {stderr}")
            
            except subprocess.TimeoutExpired:
                error_msg = "Pipeline execution timed out (300s). Please try again."
                st.error(f"❌ {error_msg}")
                frontend_logger.error(error_msg)
            except Exception as e:
                error_msg = f"Error running pipeline: {str(e)}"
                st.error(f"❌ {error_msg}")
                frontend_logger.error(error_msg)

# Info section
st.markdown("---")
st.header("📖 How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1️⃣ Code Generation")
    st.write("Google Gemini API generates Python/Flask code based on your description.")

with col2:
    st.subheader("2️⃣ GitHub Upload")
    st.write("Code is automatically pushed to a new GitHub repository under your account.")

with col3:
    st.subheader("3️⃣ Netlify Deploy")
    st.write("Repository is deployed to Netlify for instant hosting and live access.")

st.markdown("---")
st.subheader("🔧 Technology Stack")
cols = st.columns(5)
tech_stack = ["CrewAI", "Google Gemini", "GitHub API", "Netlify API", "Python"]
for col, tech in zip(cols, tech_stack):
    col.info(f"🛠️ {tech}")

st.markdown("---")
st.caption("Coding Simulation Framework | Powered by CrewAI & Google Gemini")
