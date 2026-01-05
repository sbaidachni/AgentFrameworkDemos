import asyncio
import logging
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
from src.common.naming_tools import generate_agent_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    try:
        agent_name = generate_agent_name("jokeagent")
        async with (
            AzureCliCredential() as credential,
            AzureAIClient(credential=credential).create_agent(
                name=agent_name,
                instructions="You are good at telling jokes."
            ),
        ):
            logger.info(f"Agent {agent_name} has been created successfully.")
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
