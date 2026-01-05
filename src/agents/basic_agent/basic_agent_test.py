import asyncio
import logging
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatAgent
from dotenv import load_dotenv
from src.common.naming_tools import generate_agent_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    try:
        async with (
            AzureCliCredential() as credential,
            AzureAIClient(credential=credential) as client,
            ChatAgent(
                chat_client=client, name=generate_agent_name("jokeagent")) as agent
        ):
            result = await agent.run("Tell me a joke about a pirate.")
            logger.info(result.text)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
