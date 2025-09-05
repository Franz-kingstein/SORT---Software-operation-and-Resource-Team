# Model API configuration for CrewAI orchestrator
# Loads secrets from environment variables (use a local .env file for dev)

import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

MODELS = {
    "mistral": {
        "base_url": os.getenv("MISTRAL_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        "api_key": os.getenv("MISTRAL_API_KEY"),
        "model": os.getenv("MISTRAL_MODEL", "mistralai/mistral-nemotron"),
    },
    "qwen": {
        "base_url": os.getenv("QWEN_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        "api_key": os.getenv("QWEN_API_KEY"),
        "model": os.getenv("QWEN_MODEL", "qwen/qwen3-coder-480b-a35b-instruct"),
    },
    "llama": {
        "base_url": os.getenv("LLAMA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        "api_key": os.getenv("LLAMA_API_KEY"),
        "model": os.getenv("LLAMA_MODEL", "meta/llama-3.1-70b-instruct"),
    },
}
