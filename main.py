"""
This is a simple MCP server that can search the web for information and fetch the content of a URL.
"""
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


model = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

server_params = StdioServerParameters(command="npx",
                                      env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
                                      args=["firecrawl-mcp"],
                                      )
client = stdio_client(server_params)


async def main() -> None:
    """
    Main function to run the MCP server.
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crwal pages, and extract data using Firecrawl tools. Think step by step and use the appropriate tools to help the user."
                }
            ]
            print("Available tools: ", *[tool.name for tool in tools])
            print("-" * 60)
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break
                messages.append({"role": "user", "content": user_input[:175000]})
                try:
                    response = await agent.arun(messages)
                    messages.append({"role": "assistant", "content": response})
                    print("Assistant: ", response)
                except Exception as e:
                    print(f"Error: {e}")
                    print("Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
