import os

os.environ["LANGCHAIN_TRACING"] = "true"

import openai
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_community.agent_toolkits.load_tools import load_tools
# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv


# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

openai_client = openai.OpenAI()

# Setting the Environment Variables
openai_client.api_key  = os.getenv('OPENAI_API_KEY')

def multiplier(a, b):
    return a * b

def parse_multiplier(string):
    a, b = string.split(",")
    return multiplier(int(a), int(b))


def main():
    llm = OpenAI(temperature=0.5)
    tools = [
        Tool(
            name= "Multiplier",
            func= parse_multiplier,
            description= "useful for when you need to multiply two numbers together. \
                The input to this tool should be a comma separated list of numbers of length two, \
                representing the two numbers you want to multiply together. For example, `1,2` would \
                be the input if you wanted to multiply 1 by 2."            
        )
    ]

    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


if __name__ == "__main__":
    
    agent_executor = main()

    agent_executor.invoke(
        {
            "input": "3 times four?",
        }
    )