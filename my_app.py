"""
My Test Autogen Application
"""

import autogen


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