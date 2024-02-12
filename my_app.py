"""
My Test Autogen Application
"""

import os
import autogen
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv


print("Starting program...\n")

######################### Configure LLM #########################

# Import config from json
config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-35-turbo-16k"]
    }
)

# Configure the LLM
my_llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

######################### Define Agents #########################

# User proxy
user_agent = UserProxyAgent(
    name='user',
    system_message="A human administrator.",
    code_execution_config={
        'work_dir': 'coding',
        'last_n_messages': 3,
        'use_docker': True
    },
    max_consecutive_auto_reply=5,
    human_input_mode="TERMINATE"
)

# Data scientist
data_science_agent = AssistantAgent(
    name='data_scientist',
    system_message="""
        Data Scientist. You are a data science and analytics expert. You are capable of building insightful analyses
        of various data using mathematical and statistical methods. You are also proficient in designing
        creative use cases for datasets that solve some business or orgainzational problem.""",
    code_execution_config=False,
    llm_config=my_llm_config
)

# Developer
dev_agent = AssistantAgent(
    name='developer',
    system_message="""
        Developer. You follow an approved plan. 
        You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code.
        So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes.
        If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption,
        collect additional info you need, and think of a different approach to try.
    """,
    code_execution_config=False,
    llm_config=my_llm_config
)

# Product manager
pm_agent = AssistantAgent(
    name='product_manager',
    system_message="""
        Product Manager.
        You are are an expert in software product management. You are capable of devising innovative and creative software products.
        You are responsible for identifying the customer need and the larger business objectives that a product or feature will fulfill.
        """,
    code_execution_config=False,
    llm_config=my_llm_config
)

# Clinician
clinician_agent = AssistantAgent(
    name='clinician',
    system_message="""
        Clinician. You are an expert in clinical medicine, pharmaceuticals, healthcare services, and clinical data analysis.
        You can devise sophisticated yet insightful analyses of different clinical conditions, outcomes, and treatments.
        Specifically, you are capable of designing research studies centered around clinical data and quality metrics.
        """,
        code_execution_config=False,
        llm_config=my_llm_config
)

# Planner
planner_agent = AssistantAgent(
    name='planner',
    system_message="""
        Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
        The plan may involve a developer who can write code, a scientist who doesn't write code,
        a clinician who doesn't write code, and a product manager who doesn't write code.
        Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
        """,
    code_execution_config=False,
    llm_config=my_llm_config
)

# Executor
executor_agent = UserProxyAgent(
    name='executor',
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "coding",
        "use_docker": True
    }
)

# Quality checker
quality_agent = AssistantAgent(
    name='quality_check',
    system_message="""
        Quality critic. Double check plan, claims, code from other agents and provide feedback.
        Check whether the plan includes adding verifiable info such as source URL.
        """,
    code_execution_config=False,
    llm_config=my_llm_config
)


######################### Construct Chat and Manager #########################

# Group chat
groupchat = autogen.GroupChat(agents=[user_agent, data_science_agent, dev_agent,
                                      pm_agent, clinician_agent, quality_agent,
                                      planner_agent, executor_agent
                                      ],
                                      messages=[],
                                      max_round=12)

# Chat manager
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=my_llm_config)


######################### Initiate Conversation #########################

# Initiate chat
initial_message = """
    Work as a team to develop a list of potential data science projects focused on
    the market for the drug Dupixent. These potential projects would be completed for
    the manufacturers of Dupixent. Therefore, please focus on analyses that would provide
    insight and value to the manufacturers of Dupixent. Use Python to create a markdown
    table showing the following information about each project:
    - The project title.
    - A short description of the project.
    - Data sources required for the project.
    - Key performance metrics for success of the project.

    Save the markdown table to a file in the current working directory named "dpx_projects.md".
"""

user_agent.initiate_chat(
    recipient=manager,
    message=initial_message
)

print("Finishing program...\n")
