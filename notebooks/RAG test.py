

###  all code taken and edited from Langchain RAG documentation

import os
import openai
from langchain import hub
from langchain.agents import AgentExecutor, AgentType, load_tools, initialize_agent, create_react_agent
from langchain_community.chat_models import ChatAnyscale
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

#RAG dependencies?
from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import format_document
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.runnables import RunnableParallel

#env variables, only for api key right now
from dotenv import load_dotenv
load_dotenv()


vectorstore = FAISS.from_texts(
    ["Callum Stoneshield is a mountain dwarf, aged 199, approaching the end of his middle years and relearning what it means to be an adventurer and to face danger for the sake of other people. Callum has lived a slow, calm life, only punctuated by couple decades or so of low stakes adventuring in his youth, and the glowing, boundless joy of his marriage to the halfling man named Coremin Dandelion. After spending adulthood settled in a small town in Estagund, working with exquisite slowness and care on his craft, Callum lived through Coremin’s twilight years and put him in the ground when he died of old age. Now widowed, grieving but happy to have spent 100 years with his beloved, he realized the speed of commerce and the world around him was too fast without his husband. It would have been difficult to keep his house, and his dedication to true craftsmanship at the same time. A few years of trying to keep living in the small, commercial town without Coremin brought Callum to a crossroads. He could try and teach his old brain new tricks and fumble through the commercial world, he could make the long, long trek back to his dwarven homeland and hope to find a place to retire with what he had saved of his work, or he could set out into the world and finally see a bit more of it and live with a bit more risk. He chose the last one, lifting his rusted, outdated rapier off of its place on the wall, selling his home, and marching off into the world. Planning a meandering trek from East to West, and attracted by stories of ruins so old they seemed to have a will of their own, Callum booked passage to Raurin the Dust Desert. It was only when he arrived that he realized he couldn’t easily leave, but he’s making the best of it."], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


print(chain.invoke("Can you tell me about Mr. Stoneshield's husband?"))

template = """Answer the question based only on the following context:
{context}

Question: {question}

Answer in the following language: {language}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "language": itemgetter("language"),
    }
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke({"question": "Can you tell me about Mr. Stoneshield's husband?", "language": "english"}))