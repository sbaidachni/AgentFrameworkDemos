import asyncio
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatAgent
from dotenv import load_dotenv
import src.common.naming_tools as naming_tools

async def main():
    load_dotenv()
    async with (
        AzureCliCredential() as credential,
        AzureAIClient(credential=credential) as client,
        ChatAgent(
            chat_client=client, name=generate_agent_name("jokeagent")) as agent
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
