#!/usr/bin/env python3
"""
Text Classification MCP Server using Static Embeddings from Model2Vec

This MCP server provides text classification functionality using static embeddings
from the Model2Vec library (Minish Lab). It allows users to classify text into
predefined category buckets using efficient static embeddings.

Requirements:
- mcp[cli]
- model2vec
- numpy
- scikit-learn

Installation:
pip install "mcp[cli]" model2vec numpy scikit-learn

Usage:
python text_classifier_server.py
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
from fastmcp import FastMCP
from model2vec import StaticModel
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("text-classifier-server")

# Global variables for the model and categories
model: Optional[StaticModel] = None
categories: Dict[str, np.ndarray] = {}
category_descriptions: Dict[str, str] = {}

def load_model():
    """Load the Model2Vec static embedding model"""
    global model
    try:
        # Load a pre-trained Model2Vec model
        # Using the potion-base-8M model which is efficient and performant
        model = StaticModel.from_pretrained("minishlab/potion-base-8M")
        logger.info("Successfully loaded Model2Vec model: minishlab/potion-base-8M")
    except Exception as e:
        logger.error(f"Failed to load Model2Vec model: {e}")
        raise

def setup_default_categories():
    """Setup default text classification categories with their embeddings"""
    global categories, category_descriptions, model
    
    if model is None:
        raise ValueError("Model not loaded")
    
    # Define default categories and their descriptions
    default_categories = {
        "technology": "Technology, software, computers, programming, artificial intelligence, gadgets",
        "business": "Business, finance, economics, marketing, entrepreneurship, corporate",
        "health": "Health, medicine, fitness, wellness, healthcare, medical research",
        "sports": "Sports, athletics, games, competition, teams, fitness activities",
        "entertainment": "Movies, music, television, celebrities, arts, culture, gaming",
        "politics": "Politics, government, elections, policy, legislation, political news",
        "science": "Science, research, discoveries, experiments, academic studies, innovation",
        "education": "Education, learning, schools, universities, teaching, academic",
        "travel": "Travel, tourism, destinations, vacation, transportation, geography",
        "food": "Food, cooking, restaurants, recipes, nutrition, culinary arts"
    }
    
    # Generate embeddings for each category using their descriptions
    for category, description in default_categories.items():
        try:
            # Create embedding for the category description
            embedding = model.encode([description])[0]
            categories[category] = embedding
            category_descriptions[category] = description
            logger.info(f"Setup category: {category}")
        except Exception as e:
            logger.error(f"Failed to setup category {category}: {e}")

@mcp.tool()
def classify_text(text: str, top_k: int = 3) -> str:
    """
    Classify text into predefined categories using static embeddings.
    
    Args:
        text: The text to classify
        top_k: Number of top categories to return (default: 3)
    
    Returns:
        JSON string with classification results
    """
    if model is None:
        return json.dumps({"error": "Model not loaded"})
    
    if not categories:
        return json.dumps({"error": "No categories defined"})
    
    try:
        # Generate embedding for the input text
        text_embedding = model.encode([text])[0]
        
        # Calculate similarities with all categories
        similarities = {}
        for category, category_embedding in categories.items():
            # Reshape for cosine similarity calculation
            text_emb = text_embedding.reshape(1, -1)
            cat_emb = category_embedding.reshape(1, -1)
            
            similarity = cosine_similarity(text_emb, cat_emb)[0][0]
            similarities[category] = float(similarity)
        
        # Sort by similarity and get top_k results
        sorted_categories = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        top_categories = sorted_categories[:top_k]
        
        # Format results
        results = {
            "text": text,
            "predictions": [
                {
                    "category": category,
                    "confidence": round(similarity, 4),
                    "description": category_descriptions.get(category, "")
                }
                for category, similarity in top_categories
            ],
            "all_scores": similarities
        }
        
        return json.dumps(results, indent=2)
        
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return json.dumps({"error": f"Classification failed: {str(e)}"})

@mcp.tool()
def add_custom_category(category_name: str, description: str) -> str:
    """
    Add a new custom category for classification.
    
    Args:
        category_name: Name of the new category
        description: Description of the category to generate its embedding
    
    Returns:
        JSON string with operation result
    """
    if model is None:
        return json.dumps({"error": "Model not loaded"})
    
    try:
        # Generate embedding for the category description
        embedding = model.encode([description])[0]
        
        # Add to categories
        categories[category_name.lower()] = embedding
        category_descriptions[category_name.lower()] = description
        
        result = {
            "success": True,
            "message": f"Added category '{category_name}' successfully",
            "category": category_name.lower(),
            "description": description,
            "total_categories": len(categories)
        }
        
        logger.info(f"Added custom category: {category_name}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Failed to add category {category_name}: {e}")
        return json.dumps({
            "success": False,
            "error": f"Failed to add category: {str(e)}"
        })

@mcp.tool()
def list_categories() -> str:
    """
    List all available categories for classification.
    
    Returns:
        JSON string with all categories and their descriptions
    """
    result = {
        "total_categories": len(categories),
        "categories": [
            {
                "name": category,
                "description": description
            }
            for category, description in category_descriptions.items()
        ]
    }
    
    return json.dumps(result, indent=2)

@mcp.tool()
def batch_classify(texts: List[str], top_k: int = 1) -> str:
    """
    Classify multiple texts at once.
    
    Args:
        texts: List of texts to classify
        top_k: Number of top categories to return for each text
    
    Returns:
        JSON string with batch classification results
    """
    if model is None:
        return json.dumps({"error": "Model not loaded"})
    
    if not categories:
        return json.dumps({"error": "No categories defined"})
    
    try:
        results = []
        
        for i, text in enumerate(texts):
            # Generate embedding for the input text
            text_embedding = model.encode([text])[0]
            
            # Calculate similarities with all categories
            similarities = {}
            for category, category_embedding in categories.items():
                text_emb = text_embedding.reshape(1, -1)
                cat_emb = category_embedding.reshape(1, -1)
                similarity = cosine_similarity(text_emb, cat_emb)[0][0]
                similarities[category] = float(similarity)
            
            # Sort by similarity and get top_k results
            sorted_categories = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
            top_categories = sorted_categories[:top_k]
            
            results.append({
                "index": i,
                "text": text,
                "predictions": [
                    {
                        "category": category,
                        "confidence": round(similarity, 4)
                    }
                    for category, similarity in top_categories
                ]
            })
        
        return json.dumps({
            "batch_size": len(texts),
            "results": results
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Batch classification error: {e}")
        return json.dumps({"error": f"Batch classification failed: {str(e)}"})

@mcp.resource("categories://list")
def get_categories_resource() -> str:
    """Resource that provides the list of available categories"""
    return json.dumps({
        "resource_type": "categories",
        "description": "Available text classification categories",
        "categories": list(category_descriptions.keys()),
        "total": len(categories)
    }, indent=2)

@mcp.resource("model://info")
def get_model_info() -> str:
    """Resource that provides information about the loaded model"""
    if model is None:
        return json.dumps({"error": "Model not loaded"})
    
    return json.dumps({
        "resource_type": "model_info",
        "model_name": "minishlab/potion-base-8M",
        "model_type": "Model2Vec Static Embeddings",
        "description": "Fast static embedding model for text classification",
        "embedding_dimension": len(model.encode(["test"])[0]) if model else "unknown",
        "categories_loaded": len(categories)
    }, indent=2)

@mcp.prompt()
def classification_prompt(text: str) -> str:
    """
    Prompt template for text classification.
    
    Args:
        text: The text to classify
    """
    return f"""Please classify the following text using the available categories:

Text: "{text}"

Use the classify_text tool to analyze this text and provide:
1. The most likely category
2. Confidence scores for top categories
3. Brief explanation of why this classification makes sense

Available categories: {', '.join(category_descriptions.keys())}"""

def initialize_server():
    """Initialize the MCP server with model and categories"""
    logger.info("Initializing Text Classification MCP Server...")
    
    try:
        # Load the Model2Vec model
        load_model()
        
        # Setup default categories
        setup_default_categories()
        
        logger.info(f"Server initialized with {len(categories)} categories")
        logger.info("Available tools: classify_text, add_custom_category, list_categories, batch_classify")
        logger.info("Available resources: categories://list, model://info")
        logger.info("Available prompts: classification_prompt")
        
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        raise

def main():
    """Main function to run the MCP server"""
    # Initialize the server
    initialize_server()
    
    # Get transport from command line argument or default to stdio
    import sys
    transport = "stdio"  # Default transport
    host = "127.0.0.1"
    port = 8000
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--http" or sys.argv[1] == "--sse":
            transport = "sse"  # Use SSE transport for HTTP
            if len(sys.argv) > 2:
                port = int(sys.argv[2])
        elif sys.argv[1] == "--streamable-http":
            transport = "http"  # Use streamable HTTP transport
            if len(sys.argv) > 2:
                port = int(sys.argv[2])
    
    if transport == "stdio":
        logger.info("Running MCP server with stdio transport")
        mcp.run()
    else:
        logger.info(f"Running MCP server with {transport} transport on {host}:{port}")
        if transport == "sse":
            logger.info(f"SSE endpoint: http://{host}:{port}/sse")
            logger.info(f"Messages endpoint: http://{host}:{port}/messages")
        else:
            logger.info(f"HTTP endpoint: http://{host}:{port}/mcp")
        logger.info("You can test it with the MCP Inspector or configure Claude Desktop")
        logger.info("Use Ctrl+C to stop the server")
        mcp.run(transport=transport, host=host, port=port)

if __name__ == "__main__":
    main()