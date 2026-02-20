import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables (OpenAI API key)
load_dotenv(override=True)


async def main():
    """Main function demonstrating MCP server integration with OpenAI Agent SDK."""

    print("=" * 70)
    print("OpenAI Agent SDK + MCP Server Integration Demo")
    print("=" * 70)
    print()

    async with MCPServerStdio(
        params={"command": "python", "args": ["server.py"]}
    ) as mcp_server:

        agent = Agent(
            name="MCP Tools Agent",
            instructions="""You are a helpful assistant with access to various utility tools:
            - Calculator for arithmetic operations (add, subtract, multiply, divide)
            - Text analyzer for analyzing text content
            - Temperature converter for converting between temperature units

            Use these tools to help answer user questions accurately and concisely.""",
            mcp_servers=[mcp_server],
            model="gpt-4o-mini"
        )

        # Test 1: Calculator
        print("Test 1: Calculator")
        print("-" * 60)
        with trace("Calculator Test"):
            result = await Runner.run(agent, "What is 125 multiplied by 48?")
            print(result.final_output)
        print()

        # Test 2: Text Analyzer
        print("Test 2: Text Analyzer")
        print("-" * 60)
        with trace("Text Analyzer Test"):
            result = await Runner.run(
                agent,
                "Analyze this text: 'The Model Context Protocol makes AI integrations easy and standardized!'"
            )
            print(result.final_output)
        print()

        # Test 3: Temperature Converter
        print("Test 3: Temperature Converter")
        print("-" * 60)
        with trace("Temperature Converter Test"):
            result = await Runner.run(agent, "Convert 100 degrees Fahrenheit to Celsius")
            print(result.final_output)
        print()

        # Test 4: Multi-tool query
        print("Test 4: Multi-Tool Query")
        print("-" * 60)
        with trace("Multi-Tool Test"):
            result = await Runner.run(
                agent,
                """I need your help with three things:
                1. Calculate 456 divided by 12
                2. Convert 25 Celsius to Fahrenheit
                3. Analyze this sentence: 'Python is amazing!'
                """
            )
            print(result.final_output)
        print()

        # Test 5: Streaming response
        print("Test 5: Streaming Response")
        print("-" * 60)
        print("Streaming answer: ", end="", flush=True)
        res = Runner.run_streamed(
            agent,
            "Calculate the sum of 789 and 456, then tell me what that number is in words."
        )
        async for event in res.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end='', flush=True)
        print()
        print()

    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
