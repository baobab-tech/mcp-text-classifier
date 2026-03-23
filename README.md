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

- **Zero-install**: Just `uv run` — dependencies are declared inline (PEP 723)
- **Fast Classification**: Uses efficient static embeddings from Model2Vec
- **10 Default Categories**: Technology, business, health, sports, entertainment, politics, science, education, travel, food
- **Custom Categories**: Add your own categories with descriptions
- **Batch Processing**: Classify multiple texts at once
- **Resource Endpoints**: Access category lists and model information
- **Prompt Templates**: Built-in prompts for classification tasks

## 📋 Installation

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) package manager

### Quick Setup
No separate install step needed — dependencies are declared inline in the script (PEP 723) and resolved automatically by `uv`.

## 🏃‍♂️ Running the Server

### Stdio Transport (Local/Default)
```bash
uv run text_classifier_server.py
```

## 🔧 Configuration

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "text-classifier": {
      "command": "uv",
      "args": ["run", "/Users/olivier/DEV/mcp-text-classifier/text_classifier_server.py"]
    }
  }
}
```

### For Claude Code
```bash
claude mcp add text-classifier -- uv run /Users/olivier/DEV/mcp-text-classifier/text_classifier_server.py
```

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

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector uv run text_classifier_server.py
```

## 🔍 Troubleshooting

### Model download fails
```bash
# Manual model download
uv run python -c "from model2vec import StaticModel; StaticModel.from_pretrained('minishlab/potion-base-8M')"
```

## 📖 Technical Details

- **Model**: `minishlab/potion-base-8M` from Model2Vec
- **Similarity**: Cosine similarity between text and category embeddings
- **Performance**: ~30MB model, fast inference with static embeddings
- **Protocol**: MCP specification 2024-11-05
- **Transport**: stdio

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