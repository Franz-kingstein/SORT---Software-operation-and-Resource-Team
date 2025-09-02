# Agentix DevOps Studio - Enhanced with LangChain, CrewAI, and MiniCPM-Llama3

## 🚀 Overview

This project implements a sophisticated AI-powered DevOps agent system that integrates:

- **MiniCPM-Llama3 v2.5** for intelligent testing strategy analysis
- **LangChain** for LLM workflow orchestration and prompt chaining
- **CrewAI** for multi-agent coordination and task delegation
- **Rule-based fallbacks** for robust operation without AI dependencies

## 🎯 Key Features

### 1. Enhanced CTO Agent Orchestrator
- **File**: `enhanced_cto_agent.py`
- **Capabilities**:
  - LangChain-powered project analysis
  - CrewAI agent coordination
  - Multiple LLM provider support (OpenAI, Anthropic, Ollama)
  - Fallback to rule-based analysis

### 2. Intelligent Testing Agent with MiniCPM-Llama3
- **File**: `enhanced_testing_agent.py`
- **Features**:
  - AI-powered test strategy recommendation
  - Functional and nonfunctional test type selection
  - Context-aware testing approach
  - Tool and framework recommendations
  - Natural language explanations

### 3. Enhanced Frontend Agent
- **File**: `agents/frontend_coder_agent.py`
- **Enhanced with**:
  - LangChain tool integration
  - Template-based code generation
  - Responsive design capabilities
  - AI-powered requirement analysis

### 4. Integrated Testing Agent
- **File**: `agents/tester_agent.py`
- **Features**:
  - Integration with enhanced testing agent
  - Automated test file generation
  - Multiple testing framework support
  - AI-driven test strategy implementation

## 🛠️ Installation and Setup

### Quick Start
```bash
# Clone and setup
git clone <repository>
cd agentix-devops-studio

# Run setup script
chmod +x setup.sh
./setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install core dependencies
pip install langchain>=0.1.0 crewai>=0.28.0

# Install MiniCPM-Llama3 dependencies
pip install transformers>=4.36.0 torch>=2.0.0 accelerate bitsandbytes

# Install OpenAI/Anthropic (optional)
pip install openai anthropic

# Install development tools
pip install pytest selenium locust
```

## 🧪 Usage Examples

### 1. Complete Integration Demo
```python
from demo_complete_integration import AgentixDevOpsStudio
import asyncio

async def demo():
    # Initialize with AI mode
    studio = AgentixDevOpsStudio(use_ai_mode=True, use_mock=True)
    
    # Process project request
    result = await studio.process_project_request(
        project_description="Real-time trading platform API",
        scenario="High security and uptime required, heavy concurrent usage"
    )
    
    print(f"Generated {len(result['files_generated'])} files")
    print(f"Used agents: {result['agents_used']}")

asyncio.run(demo())
```

### 2. Enhanced Testing Agent
```python
from enhanced_testing_agent import EnhancedTestingAgent

# Initialize agent
agent = EnhancedTestingAgent(use_mock=True)  # Set False for real GPU inference

# Analyze project
strategy = agent.analyze_project(
    project_description="E-commerce web application",
    scenario="Payment processing, mobile support, high availability"
)

print(f"Recommended functional tests: {strategy['functional_tests']}")
print(f"Recommended nonfunctional tests: {strategy['nonfunctional_tests']}")
print(f"Estimated effort: {strategy['estimated_effort']}")
```

### 3. Enhanced CTO Agent
```python
from enhanced_cto_agent import EnhancedCTOAgent
import asyncio

async def analyze():
    # Initialize CTO agent
    cto = EnhancedCTOAgent(model_provider="openai", use_fallback=True)
    
    # Process user request
    result = await cto.process_user_request(
        "Build a microservices architecture with authentication and real-time notifications"
    )
    
    print("Task assignments:", result['task_assignments'])

asyncio.run(analyze())
```

## 🤖 AI Model Configuration

### OpenAI Configuration
```bash
# In .env file
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL_PROVIDER=openai
DEFAULT_MODEL_NAME=gpt-3.5-turbo
```

### MiniCPM-Llama3 (Local GPU)
```python
# For real GPU inference
agent = EnhancedTestingAgent(
    model_name="openbmb/MiniCPM-Llama3-V-2_5",
    device="cuda",
    use_mock=False
)
```

### Ollama (Local Models)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull codellama:7b

# Configure in .env
DEFAULT_MODEL_PROVIDER=ollama
LOCAL_MODEL_NAME=codellama:7b
```

## 📊 Example Output

### Testing Strategy Recommendation
```json
{
  "functional_tests": ["unit", "integration", "system", "UAT", "regression"],
  "nonfunctional_tests": ["performance", "security", "scalability", "reliability"],
  "explanation": "For a real-time trading platform, unit and integration testing validate individual functions and module interactions. System and UAT ensure business workflows work end-to-end. Regression testing mitigates the risk of bugs with rapid releases. Given high concurrency, performance testing is necessary, while security testing addresses high-stakes financial operations. Scalability and reliability testing ensure the platform manages concurrent load and maintains uptime.",
  "test_tools": {
    "unit": "pytest, unittest",
    "integration": "pytest, Postman",
    "system": "Selenium, Robot Framework",
    "performance": "Locust, JMeter",
    "security": "OWASP ZAP, Bandit"
  },
  "priority_order": ["unit", "integration", "system", "performance", "security"],
  "estimated_effort": "High (4-6 weeks)"
}
```

## 🔧 Architecture

### Agent Hierarchy
```
Enhanced CTO Agent (Orchestrator)
├── Enhanced Testing Agent (MiniCPM-Llama3)
├── Frontend Coder Agent (LangChain Tools)
├── Backend Coder Agent
└── Basic Tester Agent (Fallback)
```

### Data Flow
```
User Request → CTO Analysis → Task Assignment → Agent Execution → Results Aggregation
     ↓              ↓              ↓                ↓                    ↓
LangChain      CrewAI         Testing          Code Generation     Final Report
Processing   Orchestration    Strategy         with AI Tools      with Recommendations
```

## 🧪 Testing Framework Support

### Functional Testing
- **Unit**: pytest, unittest, nose2
- **Integration**: pytest, Postman, REST Assured
- **System**: Selenium, Robot Framework, Cypress
- **API**: Postman, pytest, REST Assured

### Nonfunctional Testing
- **Performance**: Locust, JMeter, k6
- **Security**: OWASP ZAP, Bandit, Safety
- **Load**: JMeter, Gatling, Artillery
- **Usability**: Manual testing, UserTesting

## 🚀 Advanced Features

### 1. Intelligent Test Selection
The MiniCPM-Llama3 powered testing agent analyzes project characteristics and automatically selects appropriate test types based on:
- Domain requirements (e.g., financial = security focus)
- Technical architecture (e.g., microservices = integration testing)
- Quality attributes (e.g., real-time = performance testing)

### 2. Multi-Agent Coordination
CrewAI orchestrates multiple specialized agents:
- **Sequential processing** for dependent tasks
- **Parallel execution** for independent work
- **Result aggregation** across agents

### 3. Fallback Mechanisms
- Rule-based analysis when AI models unavailable
- Mock responses for testing without GPU
- Graceful degradation of features

## 📁 Generated Files

The system automatically generates:
- **Test files**: `tests/test_*.py`
- **Configuration**: `pytest.ini`, `requirements.txt`
- **Frontend code**: `templates/*.html`, `static/css/*.css`
- **Backend APIs**: `backend/*.py`

## 🔒 Security Considerations

- API keys stored in environment variables
- Quantized models for memory efficiency
- Input validation for all agent interactions
- Secure defaults for all configurations

## 🎯 Future Enhancements

1. **Additional LLM Models**: Support for more local models
2. **Real-time Collaboration**: Multi-user agent coordination
3. **CI/CD Integration**: Automated pipeline generation
4. **Monitoring**: Agent performance and cost tracking
5. **Custom Agents**: Domain-specific agent creation

## 📚 Documentation

- **API Reference**: See individual agent docstrings
- **Configuration Guide**: Check `.env.example`
- **Troubleshooting**: Common issues in setup script output
- **Examples**: Multiple demo scenarios included

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all demos pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using GitHub Copilot, LangChain, CrewAI, and MiniCPM-Llama3**
