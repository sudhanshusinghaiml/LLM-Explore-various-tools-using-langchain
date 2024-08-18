import os
import openai
from langchain import hub
# from langchain.python import PythonREPL
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.agents import AgentExecutor, Tool
from langchain.agents.types import AgentType
from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
from langchain_community.agent_toolkits.load_tools import load_tools
# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv


# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

openai_client = openai.OpenAI()

# Setting the Environment Variables
openai_client.api_key  = os.getenv('OPENAI_API_KEY')

def main():
    llm = OpenAI(temperature=0.5)
    agent_executor = create_python_agent(
        llm= llm,
        tool= PythonREPLTool(), 
        verbose= True,
        agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    return agent_executor


if __name__ == "__main__":
    
    agent_executor = main()

    agent_executor.run("Please help me write a program for fibonacci series")