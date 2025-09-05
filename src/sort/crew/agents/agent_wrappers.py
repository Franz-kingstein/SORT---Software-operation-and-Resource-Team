from openai import OpenAI
from .model_config import MODELS

MISTRAL_SYSTEM_PROMPT = (
    "You are a senior DevOps planner and orchestrator. "
    "Given a user goal, break it down into clear, actionable steps for an AI coding pipeline. "
    "Be concise, logical, and ensure the plan is suitable for automated code generation."
)

QWEN_SYSTEM_PROMPT = (
    "You are an expert AI coding agent. "
    "All code you generate will be executed in a sandboxed Docker container running Python 3.12, "
    "with no network access, a 256MB memory limit, and no external dependencies unless explicitly specified by the user. "
    "Given a plan or task, generate correct, minimal, and production-ready code that will run successfully in this environment. "
    "Focus on clarity, best practices, and do not include explanations or comments unless requested."
)

LLAMA_SYSTEM_PROMPT = (
    "You are a strict code reviewer and verifier. "
    "Given code, analyze it for syntax errors, security issues, and logic flaws. "
    "Respond with a concise verdict and a list of any problems found."
)

class MistralAgent:
    def __init__(self):
        cfg = MODELS["mistral"]
        self.client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
        self.model = cfg["model"]

    def plan(self, prompt: str, **kwargs):
        messages = [
            {"role": "system", "content": MISTRAL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.6),
            top_p=kwargs.get("top_p", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=False
        )
        return completion.choices[0].message.content

class QwenAgent:
    def __init__(self):
        cfg = MODELS["qwen"]
        self.client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
        self.model = cfg["model"]

    def generate_code(self, plan: str, **kwargs):
        messages = [
            {"role": "system", "content": QWEN_SYSTEM_PROMPT},
            {"role": "user", "content": plan},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.8),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=False
        )
        return completion.choices[0].message.content

class LlamaAgent:
    def __init__(self):
        cfg = MODELS["llama"]
        self.client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
        self.model = cfg["model"]

    def validate_code(self, code: str, **kwargs):
        messages = [
            {"role": "system", "content": LLAMA_SYSTEM_PROMPT},
            {"role": "user", "content": code},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
            top_p=kwargs.get("top_p", 0.7),
            max_tokens=kwargs.get("max_tokens", 1024),
            stream=False
        )
        return completion.choices[0].message.content
