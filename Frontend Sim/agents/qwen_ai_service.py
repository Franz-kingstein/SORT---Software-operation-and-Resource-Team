#!/usr/bin/env python3
"""
Qwen AI Service with Hugging Face Integration
=============================================

This service provides Qwen AI integration using Hugging Face Transformers
for enhanced code generation across both backend and frontend development agents.

Features:
- Local Qwen model inference via Hugging Face
- Code generation with Qwen models
- Context-aware programming assistance
- Multi-language support
- No API costs - runs locally
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from functools import lru_cache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure network settings - some environments need this
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = "1"  # Prefer native downloader
os.environ['HF_HUB_DISABLE_EXPERIMENTAL_WARNING'] = "1"  # Reduce noise

# Hugging Face imports - enable online mode with optional token
HF_AVAILABLE = False
try:
    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    from huggingface_hub import hf_hub_download
    logger.info(f"📦 Torch version: {torch.__version__}")
    logger.info(f"📦 Transformers version: {transformers.__version__}")
    HF_AVAILABLE = True
    logger.info("🤗 Hugging Face Transformers available (online mode; anonymous by default)")
except ImportError as e:
    logger.warning(f"⚠️ Hugging Face Transformers not available: {e}")
except Exception as e:
    logger.warning(f"⚠️ Error initializing Transformers stack: {e}")


@dataclass
class AIResponse:
    """Response from AI service."""
    success: bool
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    error: Optional[str] = None


class QwenAIService:
    """
    Qwen AI service using Hugging Face for enhanced code generation.
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize Qwen AI service with Hugging Face.
        
        Args:
            model_name: Model name (default: gpt2 for testing)
        """
        # Use a smaller model for first-run reliability (public model)
        requested_model = model_name or "distilgpt2"
        # Allow user to place a manual local copy under ./local_models/<model_name>
        local_dir = os.path.join(os.getcwd(), "local_models", requested_model)
        if os.path.isdir(local_dir):
            self.model_name = local_dir  # Transformers accepts a local path
            logger.info(f"📂 Using local model directory: {local_dir}")
        else:
            self.model_name = requested_model
        self.max_tokens = 512  # Smaller for GPT2
        self.temperature = 0.3
        
        # Ensure we are NOT in forced offline mode from a previous session
        for flag in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE"):
            if os.environ.get(flag) == '1':
                logger.info(f"🌐 Removing stale offline flag: {flag}")
                os.environ.pop(flag, None)
        enable_hf = os.getenv("ENABLE_HF", "0").lower() in ["1", "true", "yes", "on"]
        if not enable_hf:
            self.initialized = False
            self.device = "cpu"
            logger.info("🧩 ENABLE_HF not set (or false) — running in template fallback mode only.")
            return

        if HF_AVAILABLE:
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                # If a token is set but invalid (causing public model 401), attempt anonymous fallback
                invalid_token = False
                hf_token_env = os.getenv("HUGGINGFACE_HUB_TOKEN") or os.getenv("HF_API_TOKEN")
                if hf_token_env:
                    try:
                        from huggingface_hub import whoami
                        whoami()  # will raise if invalid
                    except Exception as who_err:
                        logger.warning(f"🔐 Provided HF token appears invalid; proceeding anonymously: {who_err}")
                        # Remove token from environment for this process to allow anonymous public downloads
                        os.environ.pop("HUGGINGFACE_HUB_TOKEN", None)
                        os.environ.pop("HF_API_TOKEN", None)
                        invalid_token = True
                # Disable hf_transfer for now
                os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
                # Attempt initialization
                self._initialize_model()
                self.initialized = True
                logger.info(f"✅ Qwen AI: Initialized with {self.model_name} on {self.device}")
                if invalid_token:
                    logger.info("✅ Anonymous load succeeded after ignoring invalid token.")
            except Exception as e:
                logger.error(f"❌ Failed to initialize model, reverting to fallback: {e}")
                self.initialized = False
                self.device = "cpu"
        else:
            self.initialized = False
            self.device = "cpu"
            logger.warning("⚠️ Hugging Face libs unavailable, using fallback")
    
    def _initialize_model(self):
        """Initialize the Qwen model and tokenizer."""
        if not HF_AVAILABLE:
            logger.warning("⚠️ Cannot initialize model: HF not available")
            return
            
        try:
            logger.info(f"🔄 Loading {self.model_name}...")
            
            def _load(anonymous: bool = True):
                # Try to pre-download the files using huggingface_hub directly
                try:
                    files_to_get = ["config.json", "tokenizer_config.json", "tokenizer.json", "pytorch_model.bin"]
                    for file in files_to_get:
                        hf_hub_download(
                            repo_id=self.model_name if "/" not in self.model_name else self.model_name.split("/")[1],
                            filename=file,
                            token=None,  # Always try anonymous first
                            local_files_only=False
                        )
                        logger.info(f"✓ Downloaded {file}")
                except Exception as dl_err:
                    logger.warning(f"Pre-download warning (non-fatal): {dl_err}")
                
                # Now try the actual model load
                load_kwargs = {
                    "trust_remote_code": True,
                    "local_files_only": False,
                }
                return AutoTokenizer.from_pretrained(self.model_name, **load_kwargs), AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    token=None if anonymous else (os.getenv("HUGGINGFACE_HUB_TOKEN") or os.getenv("HF_API_TOKEN"))
                )

            # First try anonymous load (public models)
            try:
                self.tokenizer, self.model = _load(anonymous=True)
            except Exception as first_err:
                if '401' in str(first_err) or 'Unauthorized' in str(first_err):
                    logger.warning("🔐 Received 401 on anonymous load (unexpected for public model)")
                else:
                    logger.warning(f"⚠️ Anonymous load failed: {first_err}; retrying with token if present")
                # Retry with token if available
                try:
                    self.tokenizer, self.model = _load(anonymous=False)
                except Exception as second_err:
                    logger.error(f"❌ Failed model load after token retry: {second_err}")
                    raise
            
            # Configure model loading based on available resources
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            }
            
            if self.device == "cuda":
                model_kwargs["device_map"] = "auto"
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
                # Set up padding token (GPT-2 doesn't have one by default)
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
                # Configure tokenizer for padding
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.model.config.pad_token_id = self.tokenizer.eos_token_id
                
                # Create generation pipeline with explicit tokenization settings
                self.generator = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    truncation=True,
                    padding=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                logger.info(f"✅ Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize model: {e}")
            raise
    
    def generate_code(self, 
                     prompt: str, 
                     language: str = "python",
                     context: Optional[Dict] = None) -> AIResponse:
        """
        Generate code using Hugging Face Qwen model.
        
        Args:
            prompt: Code generation prompt
            language: Programming language
            context: Additional context for generation
            
        Returns:
            AIResponse: Generated code and metadata
        """
        logger.info(f"📝 Generating code for prompt: {prompt[:100]}...")
        logger.info(f"🔧 Using language: {language}, context: {context}")
        
        if not self.initialized:
            logger.warning("⚠️ Model not initialized, using fallback")
            return self._fallback_generation(prompt, language, context)
        
        try:
            # Prepare the enhanced prompt
            enhanced_prompt = self._prepare_code_prompt(prompt, language, context)
            
            # Generate with Qwen model
            logger.info("🤖 Calling model for generation...")
            response = self._call_hf_model(enhanced_prompt)
            
            if response:
                logger.info(f"✅ Generated response (first 100 chars): {response[:100]}...")
                return AIResponse(
                    success=True,
                    content=response,
                    model_used=self.model_name,
                    tokens_used=len(response.split())
                )
            else:
                logger.warning("⚠️ No response from model, falling back")
                return self._fallback_generation(prompt, language, context)
                
        except Exception as e:
            logger.error(f"Qwen AI error: {str(e)}")
            return self._fallback_generation(prompt, language, context)
    
    def generate_backend_code(self, 
                            task_description: str,
                            framework: str = "fastapi",
                            requirements: Optional[Dict] = None) -> AIResponse:
        """
        Generate backend code using Qwen AI.
        
        Args:
            task_description: Description of backend task
            framework: Backend framework (fastapi, flask, django)
            requirements: Additional requirements
            
        Returns:
            AIResponse: Generated backend code
        """
        context = {
            "type": "backend",
            "framework": framework,
            "requirements": requirements or {}
        }
        
        prompt = f"""
Generate {framework} backend code for the following task:
{task_description}

Requirements:
- Use modern Python practices
- Include proper error handling
- Add type hints
- Include docstrings
- Make it production-ready
- Follow {framework} best practices

{self._format_requirements(requirements) if requirements else ""}

Generate complete, working code with proper structure.
"""
        
        return self.generate_code(prompt, "python", context)
    
    def generate_frontend_code(self, 
                             task_description: str,
                             framework: str = "vanilla",
                             requirements: Optional[Dict] = None) -> AIResponse:
        """
        Generate frontend code using Qwen AI.
        
        Args:
            task_description: Description of frontend task
            framework: Frontend framework (vanilla, react, vue)
            requirements: Additional requirements
            
        Returns:
            AIResponse: Generated frontend code
        """
        context = {
            "type": "frontend",
            "framework": framework,
            "requirements": requirements or {}
        }
        
        prompt = f"""
You are a professional frontend developer. Create a detailed, production-ready implementation for this task:
{task_description}

Technical Requirements:
- Use modern {framework} best practices
- Create a responsive, mobile-first design
- Implement proper accessibility (ARIA labels, semantic HTML)
- Add comprehensive error handling
- Include loading states and user feedback
- Use modern CSS features (Grid/Flexbox)
- Implement proper component structure
- Add TypeScript types (if applicable)
- Include proper documentation

Visual Requirements:
- Create an engaging, modern UI
- Use smooth animations and transitions
- Ensure consistent spacing and alignment
- Follow a cohesive color scheme
- Include hover and active states
- Add visual feedback for actions

{self._format_requirements(requirements) if requirements else ""}

Generate complete, working code with all necessary HTML, CSS, and JavaScript. Include any required dependencies. Structure the code properly for production use.
"""
        
        language = "javascript" if framework != "vanilla" else "html"
        return self.generate_code(prompt, language, context)
    
    def _prepare_code_prompt(self, prompt: str, language: str, context: Optional[Dict]) -> str:
        """Prepare enhanced prompt for code generation."""
        context_type = context.get("type") if context else "unknown"
        framework = context.get("framework") if context else "vanilla"
        
        system_prompt = f"""You are an expert {language} developer specializing in {framework} development. You have extensive experience building production applications.

TASK REQUIREMENTS:
{prompt}

IMPLEMENTATION NOTES:
- Generate complete, working code only (no explanations)
- Include all necessary imports and dependencies
- Add comprehensive error handling
- Use {framework} best practices and patterns
- Structure code for maintainability
- Include proper types and documentation
- Focus on production-ready code quality

Language: {language}
Context: {json.dumps(context, indent=2) if context else "None"}

Please provide:
1. Clean, well-structured code
2. Proper comments and documentation
3. Error handling where appropriate
4. Modern best practices
5. Complete working implementation

Generate only the code without explanations:

```{language}
"""
        return system_prompt
    
    def _call_hf_model(self, prompt: str) -> Optional[str]:
        """Call Hugging Face model for code generation."""
        try:
            # Generate response with creative but controlled settings
            outputs = self.generator(
                prompt,
                max_new_tokens=self.max_tokens,
                temperature=0.7,        # Moderate creativity
                do_sample=True,
                top_p=0.9,             # Nucleus sampling
                top_k=40,              # Top-k sampling
                num_return_sequences=1,
                repetition_penalty=1.2, # Reduce repetition
                return_full_text=False  # Only return the newly generated text
            )
            
            # Extract generated text
            generated_text = outputs[0]['generated_text']
            
            # Remove the prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Extract code from markdown if present
            if "```" in generated_text:
                code_blocks = generated_text.split("```")
                if len(code_blocks) >= 2:
                    # Get the first code block
                    code = code_blocks[1]
                    # Remove language identifier if present
                    lines = code.split('\n')
                    if lines and lines[0].strip() in ['python', 'javascript', 'html', 'css', 'sql']:
                        lines = lines[1:]
                    return '\n'.join(lines).strip()
            
            return generated_text.strip()
                
        except Exception as e:
            logger.error(f"Hugging Face model call failed: {str(e)}")
            return None
    
    def _fallback_generation(self, prompt: str, language: str, context: Optional[Dict]) -> AIResponse:
        """Fallback code generation when Qwen is not available."""
        logger.info("Using fallback code generation")
        
        if language == "python":
            code = self._generate_python_template(prompt, context)
        elif language in ["javascript", "html"]:
            code = self._generate_web_template(prompt, context)
        else:
            code = f"# TODO: Implement {prompt}\n# Language: {language}\n"
        
        return AIResponse(
            success=True,
            content=code,
            model_used="template_fallback"
        )
    
    def _generate_python_template(self, prompt: str, context: Optional[Dict]) -> str:
        """Generate basic Python template."""
        framework = context.get("framework", "fastapi") if context else "fastapi"
        
        if "api" in prompt.lower() and framework == "fastapi":
            return '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        elif "auth" in prompt.lower():
            return '''from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register")
async def register(user: UserCreate):
    # TODO: Hash password and save to database
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserCreate):
    # TODO: Verify credentials
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
'''
        else:
            return f'''# {prompt}
# Generated Python code template

def main():
    """Main function."""
    print("Implementation needed")

if __name__ == "__main__":
    main()
'''
    
    def _generate_web_template(self, prompt: str, context: Optional[Dict]) -> str:
        """Generate basic web template."""
        if "login" in prompt.lower() or "auth" in prompt.lower():
            return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background-color: #f5f5f5; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .error { color: red; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <div class="error" id="usernameError"></div>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <div class="error" id="passwordError"></div>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Simple validation
            if (!username) {
                document.getElementById('usernameError').textContent = 'Username is required';
                return;
            }
            if (!password) {
                document.getElementById('passwordError').textContent = 'Password is required';
                return;
            }
            
            // TODO: Send login request to backend
            console.log('Login attempt:', { username, password });
            alert('Login functionality needs backend integration');
        });
    </script>
</body>
</html>'''
        else:
            return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background-color: #007bff; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .content { background-color: #f8f9fa; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Generated Application</h1>
            <p>Built with enhanced AI capabilities</p>
        </div>
        <div class="content">
            <h2>Welcome</h2>
            <p>This is a generated web application. Implementation details should be added based on requirements.</p>
        </div>
    </div>
    <script>
        console.log("Generated application loaded");
        // TODO: Add application logic here
    </script>
</body>
</html>'''
    
    def _format_requirements(self, requirements: Dict) -> str:
        """Format requirements for the prompt."""
        if not requirements:
            return ""
        
        formatted = "Additional Requirements:\n"
        for key, value in requirements.items():
            formatted += f"- {key}: {value}\n"
        
        return formatted

    def get_status(self) -> Dict[str, Any]:
        """Return service status for health endpoint."""
        return {
            "initialized": getattr(self, "initialized", False),
            "model_name": getattr(self, "model_name", None),
            "device": getattr(self, "device", "cpu"),
            "enable_hf": os.getenv("ENABLE_HF", "0"),
            "fallback": not getattr(self, "initialized", False),
        }


# Add to qwen_ai_service.py
CACHE_DIR = os.path.join(os.getcwd(), "local_models", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Singleton instance
_qwen_service = None

def get_qwen_service() -> QwenAIService:
    """Get singleton Qwen AI service instance."""
    global _qwen_service
    if _qwen_service is None:
        _qwen_service = QwenAIService()
    return _qwen_service


# Test function
def test_qwen_service():
    """Test the Qwen AI service."""
    service = get_qwen_service()
    
    print("🧪 Testing Qwen AI Service...")
    
    # Test backend generation
    backend_result = service.generate_backend_code(
        "Create a REST API for user management with CRUD operations",
        framework="fastapi"
    )
    
    print(f"✅ Backend generation: {backend_result.success}")
    print(f"📊 Model used: {backend_result.model_used}")
    print(f"📝 Code length: {len(backend_result.content)} characters")
    
    # Test frontend generation
    frontend_result = service.generate_frontend_code(
        "Create a responsive login form with validation",
        framework="vanilla"
    )
    
    print(f"✅ Frontend generation: {frontend_result.success}")
    print(f"📊 Model used: {frontend_result.model_used}")
    print(f"📝 Code length: {len(frontend_result.content)} characters")
    
    return backend_result.success and frontend_result.success


if __name__ == "__main__":
    test_qwen_service()

# Add better caching to qwen_ai_service.py
@lru_cache(maxsize=100)
def _generate_with_cache(prompt: str, **kwargs) -> str:
    # Your existing generation code here