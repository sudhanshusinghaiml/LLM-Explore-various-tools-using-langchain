import os
from openai import OpenAI
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools


# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv


# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

openai_client = OpenAI()

# Setting the Environment Variables
openai_client.api_key  = os.getenv('OPENAI_API_KEY')


def start_chat():
    math_llm = ChatOpenAI(temperature=0.0)
    tools = load_tools(
        ["human", "llm-math"],
        llm=math_llm,
    )
    
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm= math_llm, tools= tools, prompt= prompt)
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


if __name__ == "__main__":
    
    agent_executor = start_chat()

    agent_executor.invoke(
        {
            "input": "what is my math problem and its solution?",
        }
    )