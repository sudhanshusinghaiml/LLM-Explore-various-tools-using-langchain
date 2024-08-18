import os
import openai
from langchain import hub
from langchain_community.tools.youtube.search import YouTubeSearchTool
from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, Tool, create_react_agent

# Use the below codes to load the passowrd in py or ipynb files
from dotenv import load_dotenv, find_dotenv
# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())
openai_client = openai.OpenAI()
# Setting the Environment Variables
openai_client.api_key  = os.getenv('OPENAI_API_KEY')

def main():
    
    tool = YouTubeSearchTool()

    tools = [
        Tool(
            name="YouTube Search",
            func= tool.run,
            description="useful for when you need to give links to youtube videos. \
                Remember to put https://youtube.com/ in front of every link to complete it"
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
    search_term = "Joe Rogan"
    num_results = 6  # You can set this to however many results you'd like
    # action_input = f"{search_term},{num_results}"
    
    agent_executor.invoke({"input": f"Find a YouTube video with the search term: {search_term}"})
