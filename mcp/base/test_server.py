"""
Test script for the MCP server
This script demonstrates how to interact with the MCP server programmatically
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path to import the server
sys.path.insert(0, str(Path(__file__).parent))


async def test_server():
    """Test the MCP server by simulating tool calls."""
    
    print("🧪 Testing MCP Server...\n", file=sys.stderr)
    
    # Import the tools from server
    from server import calculator, text_analyzer, temperature_converter
    
    # Test 1: Calculator
    print("Test 1: Calculator (multiply)", file=sys.stderr)
    result = await calculator("multiply", 12, 5)
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 2: Calculator (divide)
    print("Test 2: Calculator (divide)", file=sys.stderr)
    result = await calculator("divide", 100, 4)
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 3: Calculator (divide by zero)
    print("Test 3: Calculator (error handling)", file=sys.stderr)
    result = await calculator("divide", 10, 0)
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 4: Text Analyzer
    print("Test 4: Text Analyzer", file=sys.stderr)
    test_text = "The Model Context Protocol makes it easy to build AI integrations!"
    result = await text_analyzer(test_text)
    print(f"✓ Result:\n{result}\n", file=sys.stderr)
    
    # Test 5: Temperature Converter (C to F)
    print("Test 5: Temperature Converter (Celsius to Fahrenheit)", file=sys.stderr)
    result = await temperature_converter(25, "celsius", "fahrenheit")
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 6: Temperature Converter (F to C)
    print("Test 6: Temperature Converter (Fahrenheit to Celsius)", file=sys.stderr)
    result = await temperature_converter(77, "fahrenheit", "celsius")
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 7: Temperature Converter (C to K)
    print("Test 7: Temperature Converter (Celsius to Kelvin)", file=sys.stderr)
    result = await temperature_converter(0, "celsius", "kelvin")
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    # Test 8: Error handling for temperature converter
    print("Test 8: Temperature Converter (error handling)", file=sys.stderr)
    result = await temperature_converter(100, "invalid", "celsius")
    print(f"✓ Result: {result}\n", file=sys.stderr)
    
    print("✅ All tests completed successfully!", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(test_server())
