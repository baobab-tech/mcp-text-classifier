#!/usr/bin/env python3
"""
Test client for HTTP Text Classification MCP Server
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any

class MCPHTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.sse_url = f"{self.base_url}/sse"
        self.messages_url = f"{self.base_url}/messages"
        self.session_id = None

    async def initialize(self):
        """Initialize connection with the MCP server"""
        async with aiohttp.ClientSession() as session:
            # First, connect to SSE endpoint
            async with session.get(self.sse_url) as response:
                if response.status == 200:
                    print(f"✅ Successfully connected to SSE endpoint")
                    
                    # Send initialization request
                    init_request = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {},
                                "resources": {}
                            },
                            "clientInfo": {
                                "name": "test-client",
                                "version": "1.0.0"
                            }
                        }
                    }
                    
                    async with session.post(self.messages_url, json=init_request) as init_response:
                        if init_response.status == 200:
                            result = await init_response.json()
                            print(f"✅ Initialization successful: {result}")
                            return True
                        else:
                            print(f"❌ Initialization failed: {init_response.status}")
                            return False
                else:
                    print(f"❌ Failed to connect to SSE endpoint: {response.status}")
                    return False

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call a tool on the MCP server"""
        async with aiohttp.ClientSession() as session:
            request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            async with session.post(self.messages_url, json=request) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"❌ Tool call failed: {response.status}")
                    return None

    async def list_tools(self):
        """List available tools"""
        async with aiohttp.ClientSession() as session:
            request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(self.messages_url, json=request) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"❌ List tools failed: {response.status}")
                    return None

async def test_server():
    """Test the HTTP MCP server"""
    print("🧪 Testing HTTP Text Classification MCP Server")
    print("=" * 50)
    
    client = MCPHTTPClient("http://localhost:8000")
    
    # Test initialization
    print("\n1. Testing initialization...")
    if not await client.initialize():
        print("❌ Server initialization failed")
        return
    
    # Test list tools
    print("\n2. Testing list tools...")
    tools_result = await client.list_tools()
    if tools_result:
        print(f"✅ Available tools: {json.dumps(tools_result, indent=2)}")
    
    # Test classification
    print("\n3. Testing text classification...")
    classification_result = await client.call_tool("classify_text", {
        "text": "Apple announced new AI features in their latest iPhone",
        "top_k": 3
    })
    if classification_result:
        print(f"✅ Classification result: {json.dumps(classification_result, indent=2)}")
    
    # Test custom category
    print("\n4. Testing add custom category...")
    add_result = await client.call_tool("add_custom_category", {
        "category_name": "automotive",
        "description": "Cars, vehicles, automotive industry, transportation"
    })
    if add_result:
        print(f"✅ Add category result: {json.dumps(add_result, indent=2)}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_server())