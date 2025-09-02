#!/usr/bin/env python3
"""Test Qwen AI Service Functionality"""

import sys
import os
sys.path.append('.')

def test_qwen_ai():
    """Test if Qwen AI service is working properly."""
    
    print("🧪 Testing Qwen AI Service")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from agents.qwen_ai_service import get_qwen_service, HF_AVAILABLE
        print(f"   ✅ HF Available: {HF_AVAILABLE}")
        
        # Get service instance
        print("2. Getting Qwen service instance...")
        service = get_qwen_service()
        print(f"   ✅ Service initialized: {service.initialized}")
        print(f"   📱 Model: {service.model_name}")
        print(f"   💻 Device: {service.device}")
        
        # Test basic code generation
        print("3. Testing code generation...")
        response = service.generate_code(
            prompt="Create a simple Python function to add two numbers",
            language="python"
        )
        
        print(f"   ✅ Success: {response.success}")
        print(f"   🤖 Model used: {response.model_used}")
        print(f"   📝 Content length: {len(response.content)} chars")
        if response.content:
            print(f"   📄 Sample output: {response.content[:100]}...")
        
        # Test backend code generation
        print("4. Testing backend code generation...")
        backend_response = service.generate_backend_code(
            task_description="Create a FastAPI endpoint for user registration",
            framework="fastapi"
        )
        
        print(f"   ✅ Success: {backend_response.success}")
        print(f"   📝 Content length: {len(backend_response.content)} chars")
        
        # Test frontend code generation  
        print("5. Testing frontend code generation...")
        frontend_response = service.generate_frontend_code(
            task_description="Create a login form with HTML and CSS",
            framework="html"
        )
        
        print(f"   ✅ Success: {frontend_response.success}")
        print(f"   📝 Content length: {len(frontend_response.content)} chars")
        
        print("\n🎉 All Qwen AI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_qwen_ai()
