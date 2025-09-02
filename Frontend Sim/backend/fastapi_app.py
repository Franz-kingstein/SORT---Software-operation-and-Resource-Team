
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Literal
import sys
import os

# Import Qwen AI service from agents
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
from qwen_ai_service import get_qwen_service


app = FastAPI()

# Allow CORS for local frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Request model for LLM code generation
class LLMRequest(BaseModel):
    prompt: str
    task_type: Literal["backend", "frontend"] = "backend"
    framework: Optional[str] = None
    requirements: Optional[dict] = None

class Item(BaseModel):
    name: str
    description: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    service = get_qwen_service()
    return {"status": "ok", **service.get_status()}


# LLM code generation endpoint
@app.post("/llm/generate")
async def llm_generate(request: LLMRequest):
    service = get_qwen_service()
    if request.task_type == "backend":
        result = service.generate_backend_code(
            task_description=request.prompt,
            framework=request.framework or "fastapi",
            requirements=request.requirements
        )
    elif request.task_type == "frontend":
        result = service.generate_frontend_code(
            task_description=request.prompt,
            framework=request.framework or "react",
            requirements=request.requirements
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid task_type. Use 'backend' or 'frontend'.")
    return {
        "success": result.success,
        "content": result.content,
        "model_used": result.model_used,
        "tokens_used": result.tokens_used,
        "error": result.error
    }

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
