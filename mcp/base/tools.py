from agents import function_tool
from agents import Agent, Runner, trace
import asyncio


@function_tool
def calculator(operation: str, a: float, b: float) -> str:
    """Performs basic arithmetic operations (add, subtract, multiply, divide).

    Args:
        operation: The arithmetic operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number

    Returns:
        The result of the operation
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Error: Unknown operation {operation}"

    return f"Result: {a} {operation} {b} = {result}"


@function_tool
def text_analyzer(text: str) -> str:
    """Analyzes text and returns statistics (character count, word count, sentence count).

    Args:
        text: The text to analyze

    Returns:
        Text analysis statistics
    """
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')

    return f"""Text Analysis:
- Characters: {char_count}
- Words: {word_count}
- Sentences: {sentence_count}
- Average word length: {char_count / max(word_count, 1):.2f}"""


@function_tool
def temperature_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin.

    Args:
        value: Temperature value to convert
        from_unit: Source temperature unit (celsius, fahrenheit, kelvin)
        to_unit: Target temperature unit (celsius, fahrenheit, kelvin)

    Returns:
        Converted temperature value
    """
    # Convert to Celsius first
    if from_unit.lower() == "celsius":
        celsius = value
    elif from_unit.lower() == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit.lower() == "kelvin":
        celsius = value - 273.15
    else:
        return f"Error: Unknown unit {from_unit}"

    # Convert from Celsius to target
    if to_unit.lower() == "celsius":
        result = celsius
    elif to_unit.lower() == "fahrenheit":
        result = celsius * 9/5 + 32
    elif to_unit.lower() == "kelvin":
        result = celsius + 273.15
    else:
        return f"Error: Unknown unit {to_unit}"

    return f"{value}°{from_unit[0].upper()} = {result:.2f}°{to_unit[0].upper()}"


"""
OpenAI Agent SDK Tools Module
This module contains utility tools for the OpenAI Agent SDK
"""

from agents import function_tool
from openai import OpenAI
from agents import Agent, Runner, trace
import asyncio
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables (OpenAI API key)
load_dotenv(override=True)


@function_tool
def calculator(operation: str, a: float, b: float) -> str:
    """Performs basic arithmetic operations (add, subtract, multiply, divide).

    Args:
        operation: The arithmetic operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number

    Returns:
        The result of the operation
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Error: Unknown operation {operation}"

    return f"Result: {a} {operation} {b} = {result}"


@function_tool
def text_analyzer(text: str) -> str:
    """Analyzes text and returns statistics (character count, word count, sentence count).

    Args:
        text: The text to analyze

    Returns:
        Text analysis statistics
    """
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')

    return f"""Text Analysis:
- Characters: {char_count}
- Words: {word_count}
- Sentences: {sentence_count}
- Average word length: {char_count / max(word_count, 1):.2f}"""


@function_tool
def temperature_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin.

    Args:
        value: Temperature value to convert
        from_unit: Source temperature unit (celsius, fahrenheit, kelvin)
        to_unit: Target temperature unit (celsius, fahrenheit, kelvin)

    Returns:
        Converted temperature value
    """
    # Convert to Celsius first
    if from_unit.lower() == "celsius":
        celsius = value
    elif from_unit.lower() == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit.lower() == "kelvin":
        celsius = value - 273.15
    else:
        return f"Error: Unknown unit {from_unit}"

    # Convert from Celsius to target
    if to_unit.lower() == "celsius":
        result = celsius
    elif to_unit.lower() == "fahrenheit":
        result = celsius * 9/5 + 32
    elif to_unit.lower() == "kelvin":
        result = celsius + 273.15
    else:
        return f"Error: Unknown unit {to_unit}"

    return f"{value}°{from_unit[0].upper()} = {result:.2f}°{to_unit[0].upper()}"


async def main():
    """Main function demonstrating direct tool definitions with OpenAI Agent SDK."""

    print("=" * 70)
    print("OpenAI Agent SDK with Direct Tool Definitions")
    print("=" * 70)
    print()

    # Create the agent with all tools
    agent = Agent(
        name="Direct Tools Agent",
        instructions="""You are a helpful assistant with access to various utility tools:
        - Calculator for arithmetic operations
        - Text analyzer for analyzing text content
        - Temperature converter for converting between temperature units

        Use these tools to help answer user questions accurately.""",
        tools=[calculator, text_analyzer, temperature_converter],
        model="gpt-4o-mini"
    )

    print(f"[Agent] Created with {len(agent.tools)} tools registered")
    print()

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
    print("Question: What is 789 plus 456, and what's that in a sentence?")
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

    # Test 6: Complex calculation
    print("Test 6: Complex Calculation")
    print("-" * 60)
    with trace("Complex Calculation Test"):
        result = await Runner.run(
            agent,
            "Calculate (100 + 50) divided by 5, then convert that temperature from Celsius to Fahrenheit"
        )
        print(result.final_output)
    print()

    print("=" * 70)
    print("All tests completed!")
    print("Successfully demonstrated direct tool definitions with OpenAI Agent SDK")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())