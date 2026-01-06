import logging
import os
import asyncio
from unittest import result
from azure.identity.aio import AzureCliCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from azure.ai.evaluation import RelevanceEvaluator, AzureOpenAIModelConfiguration, evaluate
from agent_framework.azure import AzureAIClient
from agent_framework import ChatAgent
from src.common.naming_tools import generate_agent_name
from src.common.evaluation_target import EvaluationTarget

logger = logging.getLogger(__name__)

class BasicAgentEvaluationTarget(EvaluationTarget):

    async def __call__(self, query: str):
        """Get the agent's answer for the given query.
        Args:
            query (str): The input query.
        Returns:
            dict: The agent's answer.
        """
        async with (
            AzureCliCredential() as credential,
            AzureAIClient(credential=credential) as client,
            ChatAgent(
                chat_client=client, name=generate_agent_name("jokeagent")) as agent
            ):
            result = await agent.run(query)
        return {"answer": result.text}


def main():
    """Run evaluation for given data.
    """
    load_dotenv()
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default").token
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=os.environ.get("AZURE_AI_MODEL_ENDPOINT"),
        api_key=token,
        azure_deployment=os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        api_version=os.environ.get("AZURE_AI_MODEL_API_VERSION"),
    )

    target = BasicAgentEvaluationTarget()

    # Define a dictionary of evaluators and their aliases
    evaluators = {
        "relevanceEval": RelevanceEvaluator(model_config),
    }

    # Setup evaluator inputs (__call__ function arguments)
    evaluators_config = {
        "relevanceEval": {"column_mapping": {"query": "${data.query}", "response": "${target.answer}"}},
    }

    # Create results directory if it does not exist
    results_dir = "./results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Run evaluations
    evaluate(
        evaluation_name=f"{generate_agent_name("jokeagent")}-eval",
        data="./src/agents/basic_agent/evaluation_data/data.jsonl",
        target=target,
        evaluators=evaluators,
        evaluator_config=evaluators_config,
        azure_ai_project=os.environ.get("AZURE_AI_PROJECT_ENDPOINT"),
        output_path=f"{results_dir}/basic_agent_evaluation_results.json",
        credential=credential,
    )


if __name__ == "__main__":
    main()
