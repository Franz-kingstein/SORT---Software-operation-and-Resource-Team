#!/usr/bin/env python3
"""
Enhanced Agents Test Script
==========================

Test script to verify Qwen AI integration with both backend and frontend agents.
This script tests the enhanced functionality and demonstrates the improved capabilities.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the parent directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from agents.backend_coder_agent import BackendCoderAgent, ExecutionResult
    from agents.frontend_coder_agent import FrontendCoderAgent
    from agents.qwen_ai_service import get_qwen_service, QwenAIService
    
    print("✅ All agent modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_qwen_service():
    """Test the Qwen AI service directly."""
    print("\n🧪 Testing Qwen AI Service")
    print("=" * 50)
    
    service = get_qwen_service()
    
    if service.initialized:
        print("✅ Qwen service initialized successfully")
    else:
        print("⚠️ Qwen service running in fallback mode")
    
    # Test backend code generation
    print("\n📱 Testing backend code generation...")
    backend_result = service.generate_backend_code(
        "Create a simple user management API with CRUD operations",
        framework="fastapi"
    )
    
    print(f"Success: {backend_result.success}")
    print(f"Model used: {backend_result.model_used}")
    print(f"Code length: {len(backend_result.content)} characters")
    
    if backend_result.error:
        print(f"Error: {backend_result.error}")
    
    # Test frontend code generation
    print("\n🎨 Testing frontend code generation...")
    frontend_result = service.generate_frontend_code(
        "Create a responsive login form with validation",
        framework="vanilla"
    )
    
    print(f"Success: {frontend_result.success}")
    print(f"Model used: {frontend_result.model_used}")
    print(f"Code length: {len(frontend_result.content)} characters")
    
    if frontend_result.error:
        print(f"Error: {frontend_result.error}")


def test_backend_agent():
    """Test the enhanced backend agent."""
    print("\n🔧 Testing Enhanced Backend Agent")
    print("=" * 50)
    
    agent = BackendCoderAgent()
    
    # Test task assignment
    test_task = {
        "role": "Senior Backend Developer",
        "action": "Write code",
        "task": "Create a FastAPI application with user authentication, database models, and REST API endpoints for a task management system"
    }
    
    print(f"Agent: {agent.name}")
    print(f"AI Enhanced: {agent.ai_enhanced}")
    print(f"Task: {test_task['task']}")
    
    print("\n🚀 Executing task...")
    result = agent.execute_task(test_task)
    
    print(f"\n📊 Results:")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print(f"Files created: {len(result.files_created)}")
    
    if result.files_created:
        print("Generated files:")
        for file in result.files_created:
            print(f"  - {file}")
    
    if result.error:
        print(f"Error: {result.error}")


def test_frontend_agent():
    """Test the enhanced frontend agent."""
    print("\n🎨 Testing Enhanced Frontend Agent")
    print("=" * 50)
    
    agent = FrontendCoderAgent()
    
    # Test task assignment
    test_task = {
        "role": "Frontend Developer",
        "action": "Create UI",
        "task": "Build a responsive user interface for a task management application with login form, dashboard, and task cards"
    }
    
    print(f"Agent: {agent.name}")
    print(f"AI Enhanced: {agent.ai_enhanced}")
    print(f"Enhanced Mode: {agent.enhanced_mode}")
    print(f"Task: {test_task['task']}")
    
    print("\n🚀 Executing task...")
    result = agent.execute_task(test_task)
    
    print(f"\n📊 Results:")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print(f"Files created: {len(result.files_created)}")
    
    if result.files_created:
        print("Generated files:")
        for file in result.files_created:
            print(f"  - {file}")
    
    if result.error:
        print(f"Error: {result.error}")


def test_full_workflow():
    """Test the complete workflow with both agents."""
    print("\n🔄 Testing Complete Workflow")
    print("=" * 50)
    
    # Create project directory
    project_name = f"qwen_test_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Test backend first
    backend_agent = BackendCoderAgent()
    backend_task = {
        "role": "Senior Backend Developer",
        "action": "Create backend",
        "task": "Build a complete FastAPI backend for a todo application with user authentication, CRUD operations, and database models"
    }
    
    print("🔧 Creating backend...")
    backend_result = backend_agent.execute_task(backend_task)
    
    # Test frontend
    frontend_agent = FrontendCoderAgent()
    frontend_task = {
        "role": "Frontend Developer", 
        "action": "Create UI",
        "task": "Build a responsive frontend interface for the todo application with authentication forms and task management UI"
    }
    
    print("\n🎨 Creating frontend...")
    frontend_result = frontend_agent.execute_task(frontend_task)
    
    # Summary
    print(f"\n📋 Project Summary:")
    print(f"Backend: {'✅ Success' if backend_result.success else '❌ Failed'}")
    print(f"Frontend: {'✅ Success' if frontend_result.success else '❌ Failed'}")
    
    total_files = len(backend_result.files_created) + len(frontend_result.files_created)
    print(f"Total files generated: {total_files}")
    
    all_files = backend_result.files_created + frontend_result.files_created
    if all_files:
        print("\nAll generated files:")
        for file in all_files:
            print(f"  - {file}")


def main():
    """Main test function."""
    print("🚀 Enhanced Agents Test Suite")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test Qwen AI service
        test_qwen_service()
        
        # Test individual agents
        test_backend_agent()
        test_frontend_agent()
        
        # Test complete workflow
        test_full_workflow()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
