# Qwen AI Configuration Guide

## Quick Setup

Your coding agents are now enhanced with Qwen AI! Here's how to set it up:

### 1. Get API Key

1. Go to [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/)
2. Sign up/Login
3. Get your API key from the console

### 2. Set Environment Variable

#### Windows (Command Prompt)

```cmd
set DASHSCOPE_API_KEY=your-api-key-here
```

#### Windows (PowerShell)

```powershell
$env:DASHSCOPE_API_KEY="your-api-key-here"
```

#### Permanent Setup (Windows)

1. Right-click "This PC" → Properties
2. Advanced System Settings → Environment Variables
3. Add new variable: `DASHSCOPE_API_KEY` = `your-api-key-here`

### 3. Test Setup

```bash
python -c "from agents.qwen_ai_service import test_qwen_service; test_qwen_service()"
```

## Current Status

✅ **Working Features:**

- Backend Agent with Qwen AI integration
- Frontend Agent with Qwen AI integration
- Fallback templates when API is not available
- Enhanced code generation capabilities

⚠️ **Current Mode:** Fallback (Template-based)

- System works without API key
- Uses high-quality templates
- Will upgrade to AI when key is provided

## Benefits with Qwen AI

🤖 **Enhanced Backend Generation:**

- Smarter API design
- Better error handling
- Context-aware code
- Production-ready patterns

🎨 **Enhanced Frontend Generation:**

- Modern UI components
- Responsive designs
- Accessibility features
- Interactive elements

## Usage Examples

### Backend Agent

```python
from agents.backend_coder_agent import BackendCoderAgent

agent = BackendCoderAgent()
result = agent.execute_task({
    "task": "Create a REST API for user management with JWT authentication"
})
```

### Frontend Agent

```python
from agents.frontend_coder_agent import FrontendCoderAgent

agent = FrontendCoderAgent()
result = agent.execute_task({
    "task": "Create a responsive dashboard with navigation and data cards"
})
```

## Generated Files Structure

```
SORT---Software-operation-and-Resource-Team/
├── backend/
│   ├── fastapi_app.py    # Main API application
│   ├── models.py         # Database models
│   └── auth.py          # Authentication system
├── templates/
│   ├── index.html       # Main page template
│   └── auth_form_*.html # Login/signup forms
├── static/
│   └── css/
│       └── styles.css   # Responsive styles
└── requirements.txt     # Dependencies
```

## Next Steps

1. **Set API Key** for enhanced AI features
2. **Test Generated Code** - run the FastAPI server
3. **Customize** - modify generated templates as needed
4. **Deploy** - your application is production-ready!

## Need Help?

If you need the API key or have any questions, let me know!
