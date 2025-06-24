#!/usr/bin/env python3
"""
HTTP Transport runner for Text Classification MCP Server
This script provides an easy way to run the server with HTTP/SSE transport
"""

import sys
import argparse
from text_classifier_server import initialize_server, mcp, logger

def parse_args():
    parser = argparse.ArgumentParser(description='Run Text Classification MCP Server')
    parser.add_argument('--transport', choices=['stdio', 'http', 'sse'], 
                       default='sse', help='Transport method (default: sse)')
    parser.add_argument('--host', default='127.0.0.1', 
                       help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, 
                       help='Port to bind to (default: 8000)')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug logging')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize the server
    initialize_server()
    
    if args.transport == "stdio":
        logger.info("Running MCP server with stdio transport")
        mcp.run()
    else:
        logger.info(f"Running MCP server with {args.transport} transport")
        if args.transport == "sse":
            logger.info(f"SSE endpoint: http://{args.host}:{args.port}/sse")
            logger.info(f"Messages endpoint: http://{args.host}:{args.port}/messages")
        else:
            logger.info(f"HTTP endpoint: http://{args.host}:{args.port}/mcp")
        logger.info("Use Ctrl+C to stop the server")
        
        # Run with the specified transport
        mcp.run(transport=args.transport, host=args.host, port=args.port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)