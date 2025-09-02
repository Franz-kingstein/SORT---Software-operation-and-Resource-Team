# Qwen AI Configuration

# ====================

#

# To enable Qwen AI integration, you need to

# 1. Get an API key from Alibaba Cloud DashScope

# 2. Set the environment variable DASHSCOPE_API_KEY

# 3. Install the required packages

# Environment Variables (set these in your system or .env file)

# DASHSCOPE_API_KEY=your_api_key_here

# Installation commands

# pip install dashscope>=1.14.0

# pip install qwen-agent>=0.0.9

# Alternative: If you don't have Qwen AI API key yet

# the agents will still work with template-based fallback generation

# Example .env file content

# DASHSCOPE_API_KEY=sk-your-actual-api-key-here

# OPENAI_API_KEY=sk-your-openai-key-here (optional fallback)

# Qwen AI Models Available

# - qwen-plus (recommended for coding tasks)

# - qwen-turbo (faster, good for simple tasks)

# - qwen-max (most capable, for complex tasks)

# To get your Qwen API key

# 1. Visit: <https://dashscope.console.aliyun.com/>

# 2. Sign up/login to Alibaba Cloud

# 3. Navigate to DashScope console

# 4. Create an API key

# 5. Set it as environment variable: DASHSCOPE_API_KEY=your_key

echo "🔑 Qwen AI Configuration Guide"
echo "================================"
echo ""
echo "To enable Qwen AI integration:"
echo "1. Get API key from: <https://dashscope.console.aliyun.com/>"
echo "2. Set environment variable:"
echo "   Windows: set DASHSCOPE_API_KEY=your_key"
echo "   Linux/Mac: export DASHSCOPE_API_KEY=your_key"
echo "3. Install packages:"
echo "   pip install dashscope qwen-agent"
echo ""
echo "The agents will work with template fallbacks if no API key is provided."
