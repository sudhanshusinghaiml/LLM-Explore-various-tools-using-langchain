import os
import openai
from langchain import hub
from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_community.tools.shell.tool import ShellTool

# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv
# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())
openai_client = openai.OpenAI()
# Setting the Environment Variables
openai_client.api_key  = os.getenv('OPENAI_API_KEY')

def main():
    
    shell_tool = ShellTool()

    llm = ChatOpenAI(temperature=0)

    shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace("{", "{{").replace("}", "}}")

    # Creating the agent using a list of tools
    tools = [
        Tool(
            name="Shell Tool",
            func=shell_tool.run,
            description=shell_tool.description
        )
    ]

    agent = create_react_agent(
        llm= OpenAI(temperature=0),
        tools= tools,
        prompt = hub.pull("hwchase17/react")
    )
    
    agent_executor = AgentExecutor(
        agent= agent,
        tools= tools,
        verbose= True
    )
    
    return agent_executor


if __name__ == "__main__":
    agent_executor = main()
    
    agent_executor.invoke({"input": "create a text file called empty and inside it, add code that \
                           trains a basic convolutional neural network for 4 epochs"})
