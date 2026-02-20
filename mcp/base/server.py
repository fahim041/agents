from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("sample-tools-server")


@mcp.tool()
async def calculator(operation: str, a: float, b: float) -> str:
    """Performs basic arithmetic operations.
    
    Args:
        operation: The arithmetic operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number
    
    Returns:
        The result of the operation as a string
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
        return f"Error: Unknown operation '{operation}'. Use: add, subtract, multiply, divide"
    
    return f"Result: {a} {operation} {b} = {result}"


@mcp.tool()
async def text_analyzer(text: str) -> str:
    """Analyzes text and returns statistics.
    
    Args:
        text: The text to analyze
    
    Returns:
        Text analysis including character count, word count, sentence count, and average word length
    """
    # Count statistics
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    result = f"""
        Text Analysis:
        - Characters: {char_count}
        - Words: {word_count}
        - Sentences: {sentence_count}
        - Average word length: {char_count / max(word_count, 1):.2f}
    """
    
    return result


@mcp.tool()
async def temperature_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin.
    
    Args:
        value: Temperature value to convert
        from_unit: Source temperature unit (celsius, fahrenheit, kelvin)
        to_unit: Target temperature unit (celsius, fahrenheit, kelvin)
    
    Returns:
        The converted temperature value
    """
    # Normalize units to lowercase
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        return f"Error: Unknown unit '{from_unit}'. Use: celsius, fahrenheit, kelvin"
    
    # Convert from Celsius to target
    if to_unit == "celsius":
        result = celsius
    elif to_unit == "fahrenheit":
        result = celsius * 9/5 + 32
    elif to_unit == "kelvin":
        result = celsius + 273.15
    else:
        return f"Error: Unknown unit '{to_unit}'. Use: celsius, fahrenheit, kelvin"
    
    return f"{value}°{from_unit[0].upper()} = {result:.2f}°{to_unit[0].upper()}"


def main():
    """Run the MCP server with stdio transport."""
    # The FastMCP server automatically handles initialization and runs on stdio
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
