import os
from langchain import hub
from langchain.agents import AgentExecutor, AgentType, load_tools, initialize_agent, create_react_agent
from langchain_community.chat_models import ChatAnyscale
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

def make_agent():
    prompt = hub.pull("hwchase17/react-chat")
    llm = ChatAnyscale(
                     anyscale_api_key="esecret_r1keyywu5gf3e8mrs9y89hyhgd",
                     model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
                     temperature=0.7,
                     verbose=True)
    tools = load_tools(["llm-math", "ddg-search"], llm=llm)
    agent = create_react_agent(llm, tools, prompt)
    #agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # prompt_template = PromptTemplate.from_template(
    #     "Tell me a {adjective} joke about {content}"
    # )
    # prompt_template.format(adjective="funny", content="chickens")

    print(agent.agent.llm_chain.prompt.template)
    return agent_executor
                       
def chat_with_agent(agent: AgentExecutor, user_input: str, history: str):
    agent.invoke
    ({
        "input": user_input,
        "chat_history": history
        })
    return history

def main():
    history = ""
    while True:
        user_input = input("[Q to quit] Chat with me: ")
        if user_input == "Q": break
        history = history + chat_with_agent(make_agent(), user_input, history)
    
main()