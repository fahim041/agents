from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import os
import asyncio

load_dotenv(override=True)

async def main():
    fetch_params = {
        "command": "uvx",
        "args": ["mcp-server-fetch"],
    }

    playwright_params = {
        "command": "npx",
        "args": ["@playwright/mcp@latest", "--headless"]
    }

    instructions = """
    You browse the internet to accomplish your instructions.
    You are highly capable at browsing the internet independently to accomplish your task,
    including accepting all cookues and clicking 'not now' as appropriate to get the content you need. If one
    website isn't fruitful, you can try another. Be persistent until you have solved your assigment, trying
    different options and sites as needed.
    """

    async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=30) as server:
        # fetch_tools = await server.list_tools()
        # print("Fetched tools:", fetch_tools)

        agent = Agent(
            name="investigator",
            instructions=instructions,
            model="gpt-4.1-mini",
            mcp_servers=[server]
        )

        result = await Runner.run(agent, "Tell me what is shown currently in Netflix homepage and what are the top 3 trending movies or shows.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())