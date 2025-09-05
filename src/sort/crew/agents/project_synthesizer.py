from __future__ import annotations
import json
from typing import Dict, List, Any
from openai import OpenAI
from .model_config import MODELS

SYNTH_SYSTEM_PROMPT_BASE = (
    "You are a precise project synthesizer. Given a user goal/plan and a primary code draft, "
    "produce a minimal, runnable project consisting of one or more files. "
    "Return ONLY strict JSON with the shape: {\"files\":[{\"path\":string,\"content\":string}]}. "
    "Paths must be POSIX style. Do not include explanations. No markdown. Only JSON."
)

PROJECT_TYPE_HINTS = {
    "react": "This is a React project. Generate a minimal React app with package.json, public/index.html, src/App.jsx or src/App.tsx, and src/main.jsx or src/main.tsx. Use Vite or Create React App. Include install/build instructions in README.md.",
    "nextjs": "This is a Next.js project. Generate a minimal Next.js app with package.json, next.config.js, pages/index.js, and public/. Include install/build instructions in README.md.",
    "node": "This is a Node.js project. Generate package.json, index.js, and any needed files. Include install/run instructions in README.md.",
    "django": "This is a Django project. Generate manage.py, requirements.txt, and a minimal app structure. Include install/migrate/run instructions in README.md.",
    "flask": "This is a Flask project. Generate app.py, requirements.txt, and a minimal app structure. Include install/run instructions in README.md.",
    "python": "This is a Python project. Prefer main.py as entry point. Include requirements.txt if needed.",
}

class ProjectSynthesizer:
    def __init__(self, model_key: str = "qwen"):
        cfg = MODELS[model_key]
        self.client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
        self.model = cfg["model"]

    def synthesize(self, plan: str, primary_code: str, user_prompt: str | None = None, project_type: str = "python", **kwargs) -> Dict[str, str]:
        user_parts: List[str] = []
        if user_prompt:
            user_parts.append(f"USER_GOAL:\n{user_prompt}")
        user_parts.append(f"PLAN:\n{plan}")
        user_parts.append(f"PRIMARY_CODE:\n{primary_code}")
        if project_type in PROJECT_TYPE_HINTS:
            user_parts.append(f"PROJECT_TYPE_HINT:\n{PROJECT_TYPE_HINTS[project_type]}")
        user_msg = "\n\n".join(user_parts)

        system_prompt = SYNTH_SYSTEM_PROMPT_BASE
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
            temperature=kwargs.get("temperature", 0.2),
            top_p=kwargs.get("top_p", 0.8),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=False,
        )
        content = completion.choices[0].message.content or ""

        files: Dict[str, str] = {}
        try:
            data = json.loads(content)
            for f in data.get("files", []):
                path = f.get("path")
                text = f.get("content", "")
                if isinstance(path, str) and path.strip():
                    files[path.strip()] = text
        except Exception:
            files = {"main.py": primary_code}

        if not files:
            files = {"main.py": primary_code}
        return files
