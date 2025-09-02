# SORT - Software Operation and Resource Team

## 🚀 Enhanced Project Structure

This project implements AI-powered coding agents with Qwen AI integration for automated software development.

```
SORT---Software-operation-and-Resource-Team/
├── agents/                          # Core AI agents
│   ├── __init__.py
│   ├── agent_interface.py          # Base agent interface
│   ├── backend_coder_agent.py      # Backend development agent
│   ├── frontend_coder_agent.py     # Frontend development agent
│   ├── testing_agent.py            # Testing agent
│   └── qwen_ai_service.py          # Qwen AI integration service
│
├── backend/                         # Generated backend code
│   ├── fastapi_app.py              # Main FastAPI application
│   ├── models.py                   # Database models
│   └── auth.py                     # Authentication system
│
├── templates/                       # Frontend templates
│   ├── index.html                  # Main application template
│   └── auth_form_*.html            # Authentication forms
│
├── static/                          # Static assets
│   └── css/
│       └── styles.css              # Generated CSS styles
│
├── tests/                           # Test suite
│   ├── test_enhanced_agents.py     # Enhanced agents tests
│   ├── demo_qwen_ai.py             # Qwen AI demonstration
│   ├── test_hf_qwen.py             # Hugging Face integration tests
│   ├── test_ecommerce_*.py         # E-commerce tests
│   ├── test_social_media_*.py      # Social media tests
│   ├── test_web_*.py               # Web application tests
│   └── test_*_unit.py              # Unit tests
│
├── setup/                           # Setup and configuration
│   ├── QWEN_SETUP_GUIDE.md         # Qwen AI setup guide
│   ├── HUGGINGFACE_SETUP.md        # Hugging Face setup
│   ├── qwen_config.md              # Qwen configuration
│   ├── MINICPM_SETUP.md            # MiniCPM setup (legacy)
│   ├── setup.sh                    # Setup script
│   ├── .env.example                # Environment variables template
│   └── legacy/                     # Legacy files
│       ├── enhanced_cto_agent.py   # Old CTO agent
│       ├── main_llm_agent.py       # Old main agent
│       ├── README_ENHANCED.md      # Old enhanced README
│       ├── CLEANUP_SUMMARY.md      # Cleanup documentation
│       └── UNIFIED_SYSTEM_ANALYSIS.md # System analysis
│
├── .gitignore                       # Git ignore rules
├── README.md                        # Main project documentation
├── requirements.txt                 # Python dependencies
└── PROJECT_STRUCTURE.md            # This file
```

## 🤖 Core Components

### AI Agents (`agents/`)
- **Backend Coder Agent**: Generates FastAPI/Flask applications, database models, authentication systems
- **Frontend Coder Agent**: Creates responsive HTML/CSS/JavaScript interfaces
- **Testing Agent**: Generates and runs test suites
- **Qwen AI Service**: Provides AI-powered code generation via Hugging Face

### Generated Applications
- **Backend**: Production-ready FastAPI applications with authentication
- **Frontend**: Modern responsive web interfaces
- **Tests**: Comprehensive test suites for all components

### Setup & Configuration (`setup/`)
- Complete setup guides for all AI integrations
- Configuration templates and examples
- Legacy implementations for reference

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Qwen AI** (Optional):
   ```bash
   # Set Hugging Face token
   set HF_TOKEN=your_hugging_face_token
   ```

3. **Run Tests**:
   ```bash
   python tests/test_enhanced_agents.py
   ```

4. **Generate Applications**:
   ```python
   from agents.backend_coder_agent import BackendCoderAgent
   agent = BackendCoderAgent()
   result = agent.execute_task({"task": "Create user management API"})
   ```

## ✨ Features

- 🤖 **AI-Powered Code Generation** with Qwen AI
- 🔄 **Fallback Templates** for offline operation
- 🏗️ **Production-Ready Code** with best practices
- 🧪 **Comprehensive Testing** suite
- 📱 **Responsive Frontend** generation
- 🔒 **Secure Backend** with JWT authentication
- 🐳 **Docker Support** (coming soon)
- 🌐 **Multi-Framework Support** (FastAPI, Flask, React, Vue)

## 🔧 Enhanced Capabilities

- **Smart Code Generation**: Context-aware, production-ready code
- **Multi-Agent Coordination**: Specialized agents for different tasks
- **Local AI Processing**: Privacy-first with Hugging Face integration
- **Flexible Deployment**: Works with or without AI models
- **Extensible Architecture**: Easy to add new agents and capabilities

## 📋 Organizational Changes

### ✅ **Completed Reorganization**

1. **Test Scripts** → `tests/` folder
   - Moved `test_enhanced_agents.py`
   - Moved `demo_qwen_ai.py`
   - Moved `test_hf_qwen.py`

2. **Setup Files** → `setup/` folder
   - Moved all setup guides
   - Moved configuration files
   - Moved environment templates

3. **Legacy Files** → `setup/legacy/` folder
   - Moved old agent implementations
   - Moved outdated documentation
   - Preserved for reference

### 🗂️ **Clean Structure Benefits**

- **Better Organization**: Clear separation of concerns
- **Easy Navigation**: Logical folder structure
- **Development Ready**: Ready for team collaboration
- **Git Friendly**: Clean repository structure
- **Documentation**: Well-documented components
