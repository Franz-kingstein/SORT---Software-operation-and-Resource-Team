#!/usr/bin/env python3
"""Diagnostic script for transformers import issues"""

import sys
import time
import threading

def test_import_with_timeout():
    """Test import with timeout using threading"""
    
    import_result = {'success': False, 'error': None}
    
    def do_import():
        try:
            print("Attempting torch import...")
            import torch
            print(f"✅ Torch imported: {torch.__version__}")
            
            print("Attempting transformers import...")
            import transformers
            print(f"✅ Transformers imported: {transformers.__version__}")
            
            import_result['success'] = True
        except Exception as e:
            import_result['error'] = str(e)
    
    # Create thread for import
    import_thread = threading.Thread(target=do_import)
    import_thread.daemon = True
    import_thread.start()
    
    # Wait for up to 15 seconds
    import_thread.join(timeout=15)
    
    if import_thread.is_alive():
        print("❌ Import timed out after 15 seconds")
        return False
    elif import_result['success']:
        print("✅ Import successful")
        return True
    else:
        print(f"❌ Import failed: {import_result['error']}")
        return False

def check_environment():
    """Check environment variables and system info"""
    
    print("🔍 Environment Diagnostics")
    print("=" * 50)
    
    import os
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check relevant environment variables
    env_vars = [
        'HF_HOME', 'HF_HUB_CACHE', 'TRANSFORMERS_CACHE',
        'HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE',
        'CUDA_VISIBLE_DEVICES', 'HTTP_PROXY', 'HTTPS_PROXY'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")
    
    # Check pip list for relevant packages
    print("\n📦 Checking installed packages...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=10)
        lines = result.stdout.split('\n')
        relevant_packages = [line for line in lines if any(pkg in line.lower() 
                           for pkg in ['torch', 'transformers', 'huggingface'])]
        for pkg in relevant_packages:
            print(f"  {pkg}")
    except Exception as e:
        print(f"  Error checking packages: {e}")

if __name__ == "__main__":
    print("🧪 Transformers Import Diagnostics")
    print("=" * 60)
    
    check_environment()
    
    print("\n🔄 Testing imports with timeout...")
    success = test_import_with_timeout()
    
    if success:
        print("\n🎉 Transformers is working properly!")
    else:
        print("\n❌ Transformers import is hanging or failing")
        print("\nPossible solutions:")
        print("1. Check internet connectivity")
        print("2. Clear HuggingFace cache")
        print("3. Set offline mode: export HF_HUB_OFFLINE=1")
        print("4. Update transformers: pip install --upgrade transformers")
        print("5. Reinstall PyTorch: pip uninstall torch && pip install torch")
