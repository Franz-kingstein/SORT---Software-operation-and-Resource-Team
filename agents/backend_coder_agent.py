#!/usr/bin/env python3
"""
Backend Coder Agent (Coder1)
============================

This agent handles backend development tasks including:
- Database schema and models
- REST API endpoints
- Authentication systems
- Business logic implementation

Team Member: [ASSIGN TO BACKEND DEVELOPER]
Status: TODO - Implementation needed

Usage:
    agent = BackendCoderAgent()
    result = agent.execute_task(task_assignment)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import Qwen AI service
try:
    from .qwen_ai_service import get_qwen_service, AIResponse
    QWEN_AVAILABLE = True
except ImportError:
    try:
        from qwen_ai_service import get_qwen_service, AIResponse
        QWEN_AVAILABLE = True
    except ImportError:
        QWEN_AVAILABLE = False
        print("⚠️ Qwen AI service not available. Using fallback mode.")


@dataclass
class ExecutionResult:
    """Result of task execution."""
    success: bool
    message: str
    files_created: List[str]
    output: Optional[str] = None
    error: Optional[str] = None


class BackendCoderAgent:
    """
    Backend development agent that implements server-side functionality.
    
    Specializes in:
    - Python/Flask/FastAPI backend development
    - Database design and ORM implementation
    - REST API development
    - Authentication and authorization
    """
    
    def __init__(self):
        self.name = "Backend Coder Agent"
        self.role = "Senior Backend Developer"
        self.specialties = ["backend", "api", "database", "authentication"]
        self.supported_frameworks = ["flask", "fastapi", "django"]
        self.supported_databases = ["sqlite", "postgresql", "mysql"]
        
        # Initialize Qwen AI service
        if QWEN_AVAILABLE:
            self.qwen_service = get_qwen_service()
            self.enhanced_mode = True
            self.ai_enhanced = True
            print("🤖 Backend Agent: Enhanced with Qwen AI")
        else:
            self.qwen_service = None
            self.enhanced_mode = False
            self.ai_enhanced = False
            print("💻 Backend Agent: Running in standard mode")
    
    def execute_task(self, task_assignment: Dict[str, str]) -> ExecutionResult:
        """
        Execute the assigned backend development task.
        
        Args:
            task_assignment: Dict containing role, action, and task description
            
        Returns:
            ExecutionResult: The result of task execution
        """
        print(f"⚙️ {self.name}: Starting task execution...")
        print(f"📋 Task: {task_assignment.get('task', 'No task specified')}")
        
        try:
            task_desc = task_assignment.get('task', '').lower()
            files_created = []
            
            # Parse task requirements from description
            requirements = {
                'database': 'database' in task_desc or 'db' in task_desc,
                'api': 'api' in task_desc or 'endpoint' in task_desc,
                'authentication': 'auth' in task_desc or 'login' in task_desc,
                'models': 'model' in task_desc or 'schema' in task_desc,
                'framework': 'flask' if 'flask' in task_desc else 'fastapi'
            }
            
            # Generate API endpoints
            if requirements['api']:
                api_code = self.generate_flask_api(requirements)
                api_file = f"backend/{requirements['framework']}_app.py"
                
                # Create directory if it doesn't exist
                os.makedirs('backend', exist_ok=True)
                
                # Write API file
                with open(api_file, 'w') as f:
                    f.write(api_code)
                files_created.append(api_file)
                print(f"� Generated: {api_file}")
            
            # Generate database models
            if requirements['database'] or requirements['models']:
                models_code = self.generate_database_models(requirements)
                models_file = 'backend/models.py'
                
                with open(models_file, 'w') as f:
                    f.write(models_code)
                files_created.append(models_file)
                print(f"🗄️ Generated: {models_file}")
            
            # Generate authentication system
            if requirements['authentication']:
                auth_code = self.generate_auth_system(requirements)
                auth_file = 'backend/auth.py'
                
                with open(auth_file, 'w') as f:
                    f.write(auth_code)
                files_created.append(auth_file)
                print(f"🔐 Generated: {auth_file}")
            
            # Generate requirements.txt
            requirements_content = self.generate_requirements_file(requirements)
            req_file = 'requirements.txt'
            
            with open(req_file, 'w') as f:
                f.write(requirements_content)
            files_created.append(req_file)
            print(f"📦 Generated: {req_file}")
            
            return ExecutionResult(
                success=True,
                message=f"Backend code generated successfully! Created {len(files_created)} files.",
                files_created=files_created,
                output=f"Generated files: {', '.join(files_created)}"
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                message=f"Backend task execution failed: {str(e)}",
                files_created=[],
                error=str(e)
            )
    
    def generate_flask_api(self, requirements: Dict[str, Any]) -> str:
        """
        Generate Flask/FastAPI code based on requirements using Qwen AI.
        """
        framework = requirements.get('framework', 'fastapi')
        
        if self.ai_enhanced and self.qwen_service:
            # Use Qwen AI for enhanced code generation
            task_desc = f"Create a {framework} REST API with the following requirements: {requirements}"
            ai_response = self.qwen_service.generate_backend_code(
                task_desc, 
                framework=framework,
                requirements=requirements
            )
            
            if ai_response.success:
                return ai_response.content
            else:
                print(f"⚠️ AI generation failed, using template: {ai_response.error}")
        
        # Fallback to template-based generation
        return self._generate_api_template(framework, requirements)
    
    def generate_database_models(self, schema: Dict[str, Any]) -> str:
        """
        Generate database models based on schema using Qwen AI.
        """
        if self.ai_enhanced and self.qwen_service:
            # Use Qwen AI for enhanced model generation
            task_desc = f"Create SQLAlchemy database models with the following schema: {schema}"
            ai_response = self.qwen_service.generate_backend_code(
                task_desc,
                framework="sqlalchemy",
                requirements=schema
            )
            
            if ai_response.success:
                return ai_response.content
            else:
                print(f"⚠️ AI generation failed, using template: {ai_response.error}")
        
        # Fallback to template-based generation
        return self._generate_models_template(schema)
    
    def generate_auth_system(self, requirements: Dict[str, Any]) -> str:
        """
        Generate authentication system using Qwen AI.
        """
        auth_type = requirements.get('auth_type', 'jwt')
        
        if self.ai_enhanced and self.qwen_service:
            # Use Qwen AI for enhanced auth generation
            task_desc = f"Create a {auth_type} authentication system with the following requirements: {requirements}"
            ai_response = self.qwen_service.generate_backend_code(
                task_desc,
                framework="fastapi",
                requirements=requirements
            )
            
            if ai_response.success:
                return ai_response.content
            else:
                print(f"⚠️ AI generation failed, using template: {ai_response.error}")
        
        # Fallback to template-based generation
        return self._generate_auth_template(auth_type)
    
    def generate_requirements_file(self, requirements: Dict[str, Any]) -> str:
        """Generate requirements.txt content based on project needs."""
        base_requirements = [
            "fastapi>=0.100.0",
            "uvicorn>=0.22.0",
            "pydantic>=2.0.0",
            "sqlalchemy>=2.0.0"
        ]
        
        if requirements.get('authentication'):
            base_requirements.extend([
                "python-jose[cryptography]>=3.3.0",
                "passlib[bcrypt]>=1.7.4",
                "python-multipart>=0.0.6"
            ])
        
        if requirements.get('database'):
            db_type = requirements.get('db_type', 'sqlite')
            if db_type == 'postgresql':
                base_requirements.append("psycopg2-binary>=2.9.0")
            elif db_type == 'mysql':
                base_requirements.append("pymysql>=1.0.0")
        
        return "\n".join(base_requirements)
    
    def _generate_api_template(self, framework: str, requirements: Dict[str, Any]) -> str:
        """Generate basic API template."""
        if framework == "fastapi":
            return '''from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

app = FastAPI(title="Generated API", version="1.0.0")
security = HTTPBearer()

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

# In-memory storage (replace with database)
items_db = []

@app.get("/")
async def root():
    return {"message": "Generated API is running"}

@app.get("/items/", response_model=List[Item])
async def get_items():
    return items_db

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item.id = len(items_db) + 1
    items_db.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        else:
            return '''from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with database)
items_db = []

@app.route('/')
def root():
    return {"message": "Generated Flask API is running"}

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items_db)

@app.route('/items', methods=['POST'])
def create_item():
    item = request.get_json()
    item['id'] = len(items_db) + 1
    items_db.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in items_db:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
'''
    
    def _generate_models_template(self, schema: Dict[str, Any]) -> str:
        """Generate basic SQLAlchemy models template."""
        return '''from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    
    def _generate_auth_template(self, auth_type: str) -> str:
        """Generate basic authentication template."""
        return '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
'''


def main():
    """Test the backend coder agent."""
    agent = BackendCoderAgent()
    
    # Test task assignment
    test_task = {
        "role": "Senior Backend Developer",
        "action": "Write code",
        "task": "Implement user authentication and authorization system"
    }
    
    result = agent.execute_task(test_task)
    print(f"✅ Task completed: {result.success}")
    print(f"📝 Message: {result.message}")


if __name__ == "__main__":
    main()
