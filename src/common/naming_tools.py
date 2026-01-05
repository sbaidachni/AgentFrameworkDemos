"""This module contains utility methods that allows us to generate names for \
    for agents."""
import subprocess
import os


def generate_agent_name(agent_type: str):
    """
    Generate a unique agent name based on the current branch name as well as an input parameter.

    Parameters:
     agent_type (str): a prefix of the agent name that usually contains the pipeline name \
        that helps to generate own agent name for each pipeline in the repository.

    Returns:
        string: agent name according to the pattern
    """
    git_branch = os.environ.get("BUILD_SOURCEBRANCHNAME")

    if git_branch is None:
        git_branch = subprocess.check_output(
            "git rev-parse --abbrev-ref HEAD", shell=True, universal_newlines=True
        ).strip()

    git_branch = git_branch.split("/")[-1]
    return f"{agent_type}-{git_branch}"
