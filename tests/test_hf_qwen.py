#!/usr/bin/env python3
"""
Test Hugging Face Qwen Integration
==================================

This script tests the Hugging Face integration for Qwen AI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.qwen_ai_service import get_qwen_service

def test_hugging_face_qwen():
    """Test Hugging Face Qwen integration."""
    print("🧪 Testing Hugging Face Qwen Integration")
    print("=" * 50)
    
    service = get_qwen_service()
    
    print(f"📊 Status: {'✅ Initialized' if service.initialized else '⚠️ Fallback Mode'}")
    print(f"🤖 Model: {service.model_name}")
    print(f"💻 Device: {service.device if hasattr(service, 'device') else 'N/A'}")
    print()
    
    # Test simple code generation
    print("🔧 Testing Backend Code Generation...")
    backend_result = service.generate_backend_code(
        "Create a simple FastAPI endpoint for user registration",
        framework="fastapi"
    )
    
    print(f"Success: {backend_result.success}")
    print(f"Model used: {backend_result.model_used}")
    print(f"Code length: {len(backend_result.content)} characters")
    if backend_result.content:
        print("Generated code preview:")
        print("-" * 30)
        print(backend_result.content[:200] + "...")
    print()
    
    # Test frontend generation
    print("🎨 Testing Frontend Code Generation...")
    frontend_result = service.generate_frontend_code(
        "Create a responsive contact form with validation",
        framework="vanilla"
    )
    
    print(f"Success: {frontend_result.success}")
    print(f"Model used: {frontend_result.model_used}")
    print(f"Code length: {len(frontend_result.content)} characters")
    if frontend_result.content:
        print("Generated code preview:")
        print("-" * 30)
        print(frontend_result.content[:200] + "...")
    
    return backend_result.success and frontend_result.success

if __name__ == "__main__":
    test_hugging_face_qwen()
