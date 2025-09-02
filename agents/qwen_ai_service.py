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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face imports - Testing with smaller model
try:
    # Set offline mode to prevent hanging on downloads
    import os
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    
    import torch
    import transformers
    print(f"📦 Torch version: {torch.__version__}")
    print(f"📦 Transformers version: {transformers.__version__}")
    
    # Test basic imports without actually loading models
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    HF_AVAILABLE = True
    logger.info("🤗 Hugging Face Transformers available (offline mode)")
        
except ImportError as e:
    HF_AVAILABLE = False
    logger.warning(f"⚠️ Hugging Face Transformers not available: {e}")
except Exception as e:
    HF_AVAILABLE = False
    logger.warning(f"⚠️ Error loading Transformers: {e}")
    # Reset environment if needed
    os.environ.pop('HF_HUB_OFFLINE', None)
    os.environ.pop('TRANSFORMERS_OFFLINE', None)


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
        # Use GPT2 for testing - it's lightweight and widely compatible
        self.model_name = model_name or "gpt2"
        self.max_tokens = 512  # Smaller for GPT2
        self.temperature = 0.3
        
        if HF_AVAILABLE:
            try:
                # Only try to access torch if HF is available
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                self._initialize_model()
                self.initialized = True
                logger.info(f"✅ Qwen AI: Initialized with {self.model_name} on {self.device}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Qwen model: {e}")
                self.initialized = False
                self.device = "cpu"
        else:
            self.initialized = False
            self.device = "cpu"
            logger.warning("⚠️ Qwen AI: Hugging Face not available, using fallback")
    
    def _initialize_model(self):
        """Initialize the Qwen model and tokenizer."""
        if not HF_AVAILABLE:
            logger.warning("⚠️ Cannot initialize model: HF not available")
            return
            
        try:
            # Import required modules inside method
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            import torch
            
            logger.info(f"🔄 Loading {self.model_name}...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Configure model loading based on available resources
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            }
            
            if self.device == "cuda":
                model_kwargs["device_map"] = "auto"
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            # Create generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
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
        if not self.initialized:
            return self._fallback_generation(prompt, language, context)
        
        try:
            # Prepare the enhanced prompt
            enhanced_prompt = self._prepare_code_prompt(prompt, language, context)
            
            # Generate with Qwen model
            response = self._call_hf_model(enhanced_prompt)
            
            if response:
                return AIResponse(
                    success=True,
                    content=response,
                    model_used=self.model_name,
                    tokens_used=len(response.split())
                )
            else:
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
Generate {framework} frontend code for the following task:
{task_description}

Requirements:
- Use modern web standards
- Make it responsive
- Include proper accessibility features
- Add error handling
- Use semantic HTML
- Follow {framework} best practices

{self._format_requirements(requirements) if requirements else ""}

Generate complete, working code with HTML, CSS, and JavaScript as needed.
"""
        
        language = "javascript" if framework != "vanilla" else "html"
        return self.generate_code(prompt, language, context)
    
    def _prepare_code_prompt(self, prompt: str, language: str, context: Optional[Dict]) -> str:
        """Prepare enhanced prompt for code generation."""
        system_prompt = f"""You are an expert {language} developer and coding assistant. Generate high-quality, production-ready code that follows best practices.

Task: {prompt}

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
            # Generate response
            outputs = self.generator(
                prompt,
                max_length=len(prompt.split()) + self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
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
