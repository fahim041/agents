"""
OpenAI Agent SDK Example with MCP Server Integration
This script demonstrates how to connect to an MCP server and use its tools with the OpenAI Agent SDK
"""

import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool import function_tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables (OpenAI API key)
load_dotenv(override=True)


async def create_mcp_tool_wrappers(session, mcp_tools):
    """Create OpenAI Agent SDK compatible tool wrappers for MCP tools."""
    tool_wrappers = []

    for tool in mcp_tools:
        if tool.name == "calculator":
            @function_tool
            async def calculator_wrapper(operation: str, a: float, b: float) -> str:
                """Calculator tool from MCP server."""
                print(f"[MCP Tool] calculator({operation}, {a}, {b})")
                result = await session.call_tool("calculator", {"operation": operation, "a": a, "b": b})
                response = result.content[0].text if result.content else "No result"
                print(f"[MCP Result] {response}")
                return response

            tool_wrappers.append(calculator_wrapper)

        elif tool.name == "text_analyzer":
            @function_tool
            async def text_analyzer_wrapper(text: str) -> str:
                """Text analyzer tool from MCP server."""
                print(f"[MCP Tool] text_analyzer('{text[:30]}...')")
                result = await session.call_tool("text_analyzer", {"text": text})
                response = result.content[0].text if result.content else "No result"
                print(f"[MCP Result] {response[:50]}...")
                return response

            tool_wrappers.append(text_analyzer_wrapper)

        elif tool.name == "temperature_converter":
            @function_tool
            async def temperature_converter_wrapper(value: float, from_unit: str, to_unit: str) -> str:
                """Temperature converter tool from MCP server."""
                print(f"[MCP Tool] temperature_converter({value}, {from_unit}, {to_unit})")
                result = await session.call_tool("temperature_converter", {
                    "value": value,
                    "from_unit": from_unit,
                    "to_unit": to_unit
                })
                response = result.content[0].text if result.content else "No result"
                print(f"[MCP Result] {response}")
                return response

            tool_wrappers.append(temperature_converter_wrapper)

    return tool_wrappers


async def main():
    """Main function demonstrating MCP server integration with OpenAI Agent SDK."""

    print("=" * 70)
    print("OpenAI Agent SDK + MCP Server Integration Demo")
    print("=" * 70)
    print()

    # Connect to MCP server and keep session alive
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            tools_response = await session.list_tools()
            print(f"Connected! Found {len(tools_response.tools)} tools:")
            for tool in tools_response.tools:
                print(f"  - {tool.name}: {tool.description[:50]}...")
            print()

            # Create tool wrappers that use the active session
            tools = await create_mcp_tool_wrappers(session, tools_response.tools)
            print(f"[OK] Created {len(tools)} tool wrappers")
            for i, tool in enumerate(tools):
                print(f"  - Tool {i+1}: {type(tool).__name__}")
            print()

            # Create the agent with the tools
            agent = Agent(
                name="MCP Tools Agent",
                instructions="""You are a helpful assistant with access to various utility tools:
                - Calculator for arithmetic operations (add, subtract, multiply, divide)
                - Text analyzer for analyzing text content
                - Temperature converter for converting between temperature units
                
                Use these tools to help answer user questions accurately and concisely.""",
                tools=tools,
                model="gpt-4o-mini"
            )
            
            print(f"[Agent] Created with {len(tools)} tools registered")
    
    # Test 1: Calculator
    print("Test 1: Calculator")
    print("-" * 60)
    result = await Runner.run(agent, "What is 125 multiplied by 48?")
    print(f"Answer: {result.final_output_as(str)}")
    print()
    
    # Test 2: Text Analyzer
    print("Test 2: Text Analyzer")
    print("-" * 60)
    result = await Runner.run(
        agent, 
        "Analyze this text: 'The Model Context Protocol makes AI integrations easy and standardized!'"
    )
    print(f"Answer: {result.final_output_as(str)}")
    print()
    
    # Test 3: Temperature Converter
    print("Test 3: Temperature Converter")
    print("-" * 60)
    result = await Runner.run(agent, "Convert 100 degrees Fahrenheit to Celsius")
    print(f"Answer: {result.final_output_as(str)}")


if __name__ == "__main__":
    asyncio.run(main())
