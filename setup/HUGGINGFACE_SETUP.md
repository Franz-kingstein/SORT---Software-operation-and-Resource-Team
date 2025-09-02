# Hugging Face Qwen AI Setup Guide

## 🤗 Hugging Face Integration Advantages

✅ **Free to use** - No API costs
✅ **Local inference** - Better privacy
✅ **Offline capable** - Works without internet
✅ **Full control** - Choose your models
✅ **Better performance** - No network latency

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `transformers` - Hugging Face model library
- `torch` - PyTorch for model inference
- `accelerate` - Optimized model loading
- `sentencepiece` - Tokenization

### 2. Model Options

#### Recommended Models

- **Qwen/Qwen2.5-Coder-7B-Instruct** (Default) - Best for coding
- **Qwen/Qwen2.5-Coder-1.5B-Instruct** - Faster, smaller
- **Qwen/Qwen2.5-Coder-32B-Instruct** - Most powerful (requires more RAM)

### 3. Hardware Requirements

#### Minimum

- **RAM**: 8GB
- **Storage**: 5GB free space
- **Device**: CPU (works but slower)

#### Recommended

- **RAM**: 16GB+
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **Storage**: 10GB+ free space

## 🔧 Configuration

### Automatic Setup

The system automatically:

- Detects available hardware (CPU/GPU)
- Downloads models on first use
- Optimizes settings for your device

### Manual Configuration

Edit `agents/qwen_ai_service.py`:

```python
# Change model
self.model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # Smaller/faster

# Adjust generation settings
self.max_tokens = 1024  # Reduce for faster generation
self.temperature = 0.1  # Lower for more deterministic output
```

## 🧪 Testing

### Quick Test

```bash
python test_hf_qwen.py
```

### Integration Test

```bash
python test_enhanced_agents.py
```

## 📊 Performance Modes

### 1. CPU Mode (Default fallback)

- Works on any computer
- Slower generation (~30-60 seconds)
- Lower quality outputs

### 2. GPU Mode (Recommended)

- Requires NVIDIA GPU
- Fast generation (~5-10 seconds)
- High quality outputs

### 3. Hybrid Mode

- Uses GPU when available
- Falls back to CPU templates when needed
- Best of both worlds

## 🎯 Expected Performance

### First Run

- Downloads model (~3-15GB depending on model)
- Takes 2-5 minutes to initialize
- Subsequent runs are much faster

### Code Generation

- **Backend API**: 5-30 seconds
- **Frontend UI**: 5-30 seconds
- **Quality**: Professional, production-ready

## 🐛 Troubleshooting

### Common Issues

#### "Out of Memory" Error

```bash
# Switch to smaller model
# Edit qwen_ai_service.py:
self.model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
```

#### Slow Generation

```bash
# Reduce max tokens
self.max_tokens = 512
```

#### Model Download Fails

```bash
# Check internet connection
# Clear Hugging Face cache:
rm -rf ~/.cache/huggingface/
```

## 🎉 What You Get

### Enhanced Code Generation

- **Smarter APIs** - Context-aware endpoint design
- **Better UIs** - Modern, responsive components
- **Cleaner Code** - Following best practices
- **More Variety** - Different solutions for same problems

### Current vs Enhanced

| Feature | Fallback Mode | Hugging Face Mode |
|---------|---------------|-------------------|
| Speed | ⚡ Instant | 🔄 5-30 seconds |
| Quality | 📊 Good | 🌟 Excellent |
| Variety | 📋 Templates | 🎨 Creative |
| Cost | 💰 Free | 💰 Free |
| Privacy | 🔒 Local | 🔒 Local |

## 🚀 Next Steps

1. **Test the setup**: `python test_hf_qwen.py`
2. **Generate projects**: Use your enhanced agents
3. **Customize models**: Try different Qwen variants
4. **Monitor performance**: Check generation times
5. **Scale up**: Move to larger models as needed

## 💡 Tips

- **First generation is slower** (model loading)
- **GPU makes a huge difference** for speed
- **Larger models = better quality** but slower
- **Temperature controls creativity** (0.1-0.8 range)

Ready to test? Run: `python test_hf_qwen.py`
