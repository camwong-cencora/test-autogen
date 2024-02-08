"""
My Test Autogen Application
"""

import autogen
from autogen import AssistantAgent, UserProxyAgent


# Import config from json
config_list = autogen.config_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-35-turbo-16k"]
    }
)

# Configure the LLM
llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

# Define agent roles
assistant_agent = AssistantAgent("assistant", llm_config={'config_list': config_list})
user_agent = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": True})

# Initiate chat
initial_message = """
    You are a data analysis and computer programming expert.
    Plot a chart of NVDA and TESLA stock price change YTD.
"""

user_agent.initiate_chat(assistant_agent, message=initial_message)
