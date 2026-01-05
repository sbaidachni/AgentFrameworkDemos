import asyncio
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
from src.common.naming_tools import generate_agent_name

async def main():
    load_dotenv()
    async with (
        AzureCliCredential() as credential,
        AzureAIClient(credential=credential).create_agent(
            name=generate_agent_name("jokeagent"),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
