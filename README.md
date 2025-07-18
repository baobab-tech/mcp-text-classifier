# Text Classification MCP Server (Model2Vec)

**A powerful Model Context Protocol (MCP) server that provides comprehensive text classification tools using fast static embeddings from Model2Vec (Minish Lab).**

## 🛠️ Complete MCP Tools & Resources

This server provides **6 essential tools**, **2 resources**, and **1 prompt template** for text classification:

### 🏷️ Classification Tools
- **`classify_text`** - Classify single text with confidence scores  
- **`batch_classify`** - Classify multiple texts simultaneously

### 📝 Category Management Tools  
- **`add_custom_category`** - Add individual custom categories
- **`batch_add_custom_categories`** - Add multiple categories at once
- **`list_categories`** - View all available categories  
- **`remove_categories`** - Remove unwanted categories

### 📊 Resources
- **`categories://list`** - Access category list programmatically
- **`model://info`** - Get model and system information

### 💬 Prompt Templates
- **`classification_prompt`** - Ready-to-use classification prompt template

## 🚀 Key Features

- **Multiple Transports**: Supports stdio (local) and HTTP/SSE (remote) transports
- **Fast Classification**: Uses efficient static embeddings from Model2Vec
- **10 Default Categories**: Technology, business, health, sports, entertainment, politics, science, education, travel, food
- **Custom Categories**: Add your own categories with descriptions
- **Batch Processing**: Classify multiple texts at once
- **Resource Endpoints**: Access category lists and model information
- **Prompt Templates**: Built-in prompts for classification tasks
- **Production Ready**: Docker, nginx, systemd support

## 📋 Installation

### Prerequisites
- Python 3.10+
- `uv` package manager (recommended) or `pip`

### Quick Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or with uv
uv sync 
```

## 🏃‍♂️ Running the Server

### Option 1: Stdio Transport (Local/Traditional)
```bash
# Run with stdio (default - for Claude Desktop local config)
python text_classifier_server.py

# Or explicitly
python text_classifier_server.py --stdio
```

### Option 2: HTTP Transport (Remote/Web)
```bash
# Run with HTTP transport on localhost:8000
python text_classifier_server.py --http

# Run on custom port
python text_classifier_server.py --http 9000

# Use the convenience script
./start_server.sh http 8000
```

### Option 3: Using the HTTP Runner
```bash
# More options with the HTTP runner
python run_http_server.py --transport http --host 127.0.0.1 --port 8000 --debug
```

## 🔧 Configuration

### For Claude Desktop

#### Stdio Transport (Local)
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "text-classifier": {
      "command": "python",
      "args": ["path/to/text_classifier_server.py"],
      "env": {}
    }
  }
}
```

#### HTTP Transport (Remote)
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "text-classifier-http": {
      "url": "http://localhost:8000/sse",
      "env": {}
    }
  }
}
```

### For VS Code
Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "text-classifier": {
      "type": "sse",
      "url": "http://localhost:8000/sse",
      "description": "Text classification server using static embeddings"
    }
  }
}
```

### For Cursor IDE
Similar to Claude Desktop, but check Cursor's MCP documentation for the exact configuration path.

## 🛠️ Available Tools

### classify_text
Classify a single text into predefined categories with confidence scores.

**Parameters:**
- `text` (string): The text to classify
- `top_k` (int, optional): Number of top categories to return (default: 3)

**Returns:** JSON with predictions, confidence scores, and category descriptions

**Example:**
```python
classify_text("Apple announced new AI features", top_k=3)
```

### batch_classify
Classify multiple texts simultaneously for efficient processing.

**Parameters:**
- `texts` (list): List of texts to classify
- `top_k` (int, optional): Number of top categories per text (default: 1)

**Returns:** JSON with batch classification results

**Example:**
```python
batch_classify(["Tech news", "Sports update", "Business report"], top_k=2)
```

### add_custom_category
Add a new custom category for classification.

**Parameters:**
- `category_name` (string): Name of the new category
- `description` (string): Description to generate the category embedding

**Returns:** JSON with operation result

**Example:**
```python
add_custom_category("automotive", "Cars, vehicles, transportation, automotive industry")
```

### batch_add_custom_categories
Add multiple custom categories in a single operation for efficiency.

**Parameters:**
- `categories_data` (list): List of dictionaries with 'name' and 'description' keys

**Returns:** JSON with batch operation results

**Example:**
```python
batch_add_custom_categories([
    {"name": "automotive", "description": "Cars, vehicles, transportation"},
    {"name": "music", "description": "Music, songs, artists, albums, concerts"}
])
```

### list_categories
List all available categories and their descriptions.

**Parameters:** None

**Returns:** JSON with all categories and their descriptions

### remove_categories
Remove one or multiple categories from the classification system.

**Parameters:**
- `category_names` (list): List of category names to remove

**Returns:** JSON with removal results for each category

**Example:**
```python
remove_categories(["automotive", "custom_category"])
```

## 📚 Available Resources

- **`categories://list`**: Get list of available categories with metadata
- **`model://info`**: Get information about the loaded Model2Vec model and system status

## 💬 Available Prompts

- **`classification_prompt`**: Template for text classification tasks with context and instructions

**Parameters:**
- `text` (string): The text to classify

**Returns:** Formatted prompt for classification with available categories listed

## 🧪 Testing

### Test HTTP Server
```bash
# Test the HTTP server endpoints
python test_http_client.py

# Check server status
./check_server.sh

# Test with curl
curl http://localhost:8000/sse
```

### Test with MCP Inspector
```bash
# For stdio transport
mcp dev text_classifier_server.py

# For HTTP transport (start server first)
# Then connect MCP Inspector to http://localhost:8000/sse
```

## 🐳 Docker Deployment

### Basic Docker
```bash
# Build and run
docker build -t text-classifier-mcp .
docker run -p 8000:8000 text-classifier-mcp
```

### Docker Compose
```bash
# Basic deployment
docker-compose up

# With nginx reverse proxy
docker-compose --profile production up
```

## 🚀 Production Deployment

### Systemd Service
```bash
# Copy service file
sudo cp text-classifier-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable text-classifier-mcp
sudo systemctl start text-classifier-mcp
```

### Nginx Reverse Proxy
The included `nginx.conf` provides:
- HTTP/HTTPS termination
- Proper SSE headers
- Load balancing support
- SSL configuration template

## 🌐 Transport Comparison

| Feature | Stdio Transport | HTTP Transport |
|---------|----------------|----------------|
| **Use Case** | Local integration | Remote/web access |
| **Performance** | Fastest | Very fast |
| **Setup** | Simple | Requires server |
| **Scalability** | One client | Multiple clients |
| **Network** | Local only | Network accessible |
| **Security** | Process isolation | HTTP-based auth |
| **Debugging** | MCP Inspector | HTTP tools + Inspector |

## 🔍 Troubleshooting

### Common Issues

1. **Server won't start**
   ```bash
   # Check if port is in use
   lsof -i :8000
   
   # Try different port
   python run_http_server.py --port 9000
   ```

2. **Claude Desktop connection fails**
   ```bash
   # Check server status
   ./check_server.sh
   
   # Verify config file syntax
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python -m json.tool
   ```

3. **Model download fails**
   ```bash
   # Manual model download
   python -c "from model2vec import StaticModel; StaticModel.from_pretrained('minishlab/potion-base-8M')"
   ```

### Debug Mode
```bash
# Enable debug logging
python run_http_server.py --debug

# Check logs
tail -f logs/mcp_server.log
```

## 📖 Technical Details

- **Model**: `minishlab/potion-base-8M` from Model2Vec
- **Similarity**: Cosine similarity between text and category embeddings
- **Performance**: ~30MB model, fast inference with static embeddings
- **Protocol**: MCP specification 2024-11-05
- **Transports**: stdio, HTTP+SSE, Streamable HTTP

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Model2Vec](https://github.com/MinishLab/model2vec) by Minish Lab for fast static embeddings
- [Anthropic](https://anthropic.com) for the Model Context Protocol specification
- [FastMCP](https://github.com/jlowin/fastmcp) for the excellent Python MCP framework

---

**Need help?** Check the troubleshooting section or open an issue in the repository.