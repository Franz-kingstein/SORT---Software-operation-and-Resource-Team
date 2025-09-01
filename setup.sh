#!/bin/bash
# Setup script for Agentix DevOps Studio with LangChain and CrewAI

echo "🚀 Setting up Agentix DevOps Studio with Enhanced AI Integration"
echo "================================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install --upgrade setuptools wheel

# Install LangChain ecosystem
echo "🦜 Installing LangChain..."
pip install langchain>=0.1.0
pip install langchain-openai>=0.1.0
pip install langchain-community>=0.0.20
pip install langchain-core>=0.1.0

# Install CrewAI
echo "👥 Installing CrewAI..."
pip install crewai>=0.28.0

# Install optional AI providers
echo "🤖 Installing AI providers..."
pip install openai>=1.12.0
pip install anthropic>=0.8.0

# Install HuggingFace Transformers and PyTorch for MiniCPM-Llama3
echo "🤖 Installing MiniCPM-Llama3 dependencies..."
pip install transformers>=4.36.0
pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install accelerate>=0.25.0
pip install bitsandbytes>=0.41.0 || echo "⚠️ bitsandbytes installation failed (optional for quantization)"

# Install web framework dependencies
echo "🌐 Installing web frameworks..."
pip install fastapi>=0.100.0
pip install uvicorn>=0.22.0
pip install flask>=2.3.0
pip install flask-cors>=4.0.0

# Install data processing libraries
echo "📊 Installing data processing libraries..."
pip install pydantic>=2.0.0
pip install pydantic-settings>=2.0.0

# Install development tools
echo "🛠️ Installing development tools..."
pip install pytest>=7.4.0
pip install pytest-asyncio>=0.21.0
pip install black>=23.0.0
pip install flake8>=6.0.0

# Install utilities
echo "🔧 Installing utilities..."
pip install python-dotenv>=1.0.0
pip install requests>=2.31.0
pip install PyYAML>=6.0.0
pip install jinja2>=3.1.0

# Install security libraries
echo "🔒 Installing security libraries..."
pip install cryptography>=41.0.0
pip install bcrypt>=4.0.0
pip install PyJWT>=2.8.0

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️ Please edit .env file and add your API keys!"
fi

# Test the installation
echo "🧪 Testing installation..."
python3 -c "
try:
    import langchain
    import crewai
    print('✅ LangChain and CrewAI imported successfully')
    
    # Test enhanced agents
    from enhanced_cto_agent import EnhancedCTOAgent
    agent = EnhancedCTOAgent(use_fallback=True)
    print('✅ Enhanced CTO Agent initialized successfully')
    
    # Test frontend agent
    from agents.frontend_coder_agent import FrontendCoderAgent
    frontend = FrontendCoderAgent()
    print('✅ Frontend Agent initialized successfully')
    
    # Test enhanced testing agent
    from enhanced_testing_agent import EnhancedTestingAgent
    tester = EnhancedTestingAgent(use_mock=True)
    print('✅ Enhanced Testing Agent initialized successfully')
    
    # Test complete integration
    from demo_complete_integration import AgentixDevOpsStudio
    studio = AgentixDevOpsStudio(use_ai_mode=True, use_mock=True)
    print('✅ Complete integration working!')
    
    print('🎉 All components working correctly!')
    
except ImportError as e:
    print(f'⚠️ Import error: {e}')
    print('Some features may not be available')
except Exception as e:
    print(f'⚠️ Initialization error: {e}')
    print('Check your configuration')
"

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Test with: python3 demo_complete_integration.py"
echo "4. Test enhanced testing: python3 enhanced_testing_agent.py"
echo ""
echo "For MiniCPM-Llama3 with GPU:"
echo "1. Install CUDA-enabled PyTorch: pip install torch --index-url https://download.pytorch.org/whl/cu118"
echo "2. Ensure 8GB+ GPU memory available"
echo "3. Set use_mock=False in testing agent"
echo ""
echo "For local models:"
echo "1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
echo "2. Pull a model: ollama pull codellama:7b"
echo "3. Set MODEL_PROVIDER=ollama in .env"
echo ""
echo "🚀 Ready to build with AI-powered DevOps agents!"
echo "🤖 Enhanced with MiniCPM-Llama3, LangChain, and CrewAI!"
