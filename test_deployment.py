#!/usr/bin/env python3
"""
Test deployment script that bypasses AI generation to test the GitHub + Netlify pipeline
"""

import sys
import os
sys.path.append('/home/franz/Documents/SORT/src')

from agents.crew_agents import create_github_repo, deploy_to_netlify

def test_deployment():
    """Test the deployment pipeline with pre-made content"""
    
    # Pre-made HTML content (simulating AI generation)
    test_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Deployment - AI Framework</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            max-width: 800px; 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
            backdrop-filter: blur(15px);
            text-align: center;
        }
        h1 { font-size: 2.5em; margin-bottom: 30px; }
        .status { 
            background: #4CAF50; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
        }
        button { 
            background: #ff6b6b; 
            color: white; 
            border: none; 
            padding: 15px 30px; 
            border-radius: 25px; 
            font-size: 16px; 
            cursor: pointer;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Test Deployment Successful!</h1>
        <div class="status">
            <h2>✅ Deployment Pipeline Working!</h2>
            <p>This proves the GitHub + Netlify integration is functioning correctly.</p>
        </div>
        <button onclick="alert('Test successful!')">Test Button</button>
        <button onclick="document.body.style.background='linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'">Change Theme</button>
        <div style="margin-top: 30px;">
            <h3>🔧 System Status</h3>
            <p>✓ GitHub Repository: Created<br>
            ✓ File Upload: Working<br>
            ✓ Netlify Deploy: Functional<br>
            ✓ Live Site: Active</p>
        </div>
    </div>
</body>
</html>"""

    print("🧪 Testing deployment pipeline without AI generation...")
    print("=" * 60)
    
    try:
        # Step 1: Create GitHub repo
        print("📁 Creating GitHub repository...")
        repo_url = create_github_repo(test_code)
        print(f"✅ GitHub repo created: {repo_url}")
        
        # Step 2: Deploy to Netlify
        print("🌐 Deploying to Netlify...")
        netlify_result = deploy_to_netlify(repo_url)
        print(f"✅ Netlify deployment: {netlify_result}")
        
        print("=" * 60)
        print("🎉 TEST COMPLETE! Your deployment pipeline is working perfectly!")
        print("💡 The only issue was the Gemini API quota limit.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_deployment()
