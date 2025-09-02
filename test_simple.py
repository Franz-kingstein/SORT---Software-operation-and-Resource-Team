#!/usr/bin/env python3
"""Simple test to debug issues."""

import sys
import os
sys.path.append('.')

try:
    print("Testing imports...")
    # Test just the module imports without initialization
    import agents.qwen_ai_service
    print("✅ Qwen service module import successful")
    
    from agents.backend_coder_agent import ExecutionResult, BackendCoderAgent
    print("✅ Backend agent module import successful")
    
    from agents.frontend_coder_agent import FrontendCoderAgent
    print("✅ Frontend agent module import successful")
    
    # Test the AI availability without full initialization
    from agents.qwen_ai_service import HF_AVAILABLE
    print(f"✅ HF Available: {HF_AVAILABLE}")
    
    print("\nTesting agent initialization...")
    backend_agent = BackendCoderAgent()
    print(f"✅ Backend agent created: ai_enhanced={backend_agent.ai_enhanced}")
    
    frontend_agent = FrontendCoderAgent()
    print(f"✅ Frontend agent created: ai_enhanced={frontend_agent.ai_enhanced}")
    
    print("✅ All import and initialization tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
