import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchResults
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv
load_dotenv()

## Embeddings
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Set WSL IP where Ollama is running
#OLLAMA_WSL_IP = "http://127.0.0.1:11434"

## Wikipedia Agent/Tool
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results = 3, doc_content_chars_max=10000)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
wiki_tool= Tool(
    name = "Wikipedia",
    func = wiki.run,
    description = "This tool uses the Wikipedia API to search for a topic."
)

## Arxiv Agent/Tool
api_wrapper_arxiv = ArxivAPIWrapper(top_k_results = 5, doc_content_chars_max=10000)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
arxiv_tool = Tool(
    name = "arxiv",
    func = arxiv.run,
    description = "Searches arXiv for papers matching the query.",
)


## DuckDuckGo Search Agent/Tool
api_wrapper_ddg = DuckDuckGoSearchAPIWrapper(region="us-en", time="y", max_results=10)
ddg = DuckDuckGoSearchResults(
    api_wrapper=api_wrapper_ddg,
    #source = "news",
    output_format="string",
    handle_tool_error=True,
    handle_validation_error=True)
ddg_tool = Tool(
    name = "DuckDuckGo_Search",
    func = ddg.run,
    description = "Searches for search queries using the DuckDuckGo Search engine."
)

system_prompt = """
You are a helpful and detailed research assistant
that has the ability to search the web, Wikipedia, and arXiv for information on a topic.
Try to understand the query submitted by the user.
Searching the internet is MANDATORY before responding to every query.
Look for any context clues that may be present in the memory.
Provide thorough, step-by-step explanations in your responses 
and include all relevant context and details from available sources.
Make sure that your response is around 100-200 words long.
You are a highly intelligent and reflective assistant.
For every query, first provide a detailed, step-by-step explanation
of your reasoning process, then on a new line after a separator 'Final Answer:', 
give your concise final answer. Do not omit any part of your reasoning.
User query: 
"""

# Streamlit App
## App Title
st.title("Langchain - Chat with search")

api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
warning_placeholder = st.sidebar.empty()

# Ask for API key if it's not set in session state.
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.session_state.api_key = api_key
    # Only display the warning if no API key is provided.
    if not st.session_state.api_key:
        warning_placeholder.warning("Please enter your Groq API Key to proceed.")
else:
    # Once the API key is provided, clear the warning.
    warning_placeholder.empty()

if "messages" not in st.session_state:
    st.session_state["messages"] = [    
        {
            "role": "assistant",
            "content": "Hi, I am a chatbot who can search the web. How can I help you today?"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Initialize conversation memory once and persist it
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
memory = st.session_state.memory

if prompt:= st.chat_input(placeholder = "Write your query here...."):
    st.session_state.messages.append({
        "role":"user",
        "content": prompt
    })
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key = st.session_state.api_key, model_name = "Llama3-8b-8192", streaming = True)
    #llm = ChatOllama(base_url=OLLAMA_WSL_IP, model="llama3.1", streaming=True)

    tools = [wiki_tool, arxiv_tool, ddg_tool]

    search_agent = initialize_agent(
        tools = tools,
        llm = llm,
        agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        max_iterations = 10,
        memory = memory,
        handle_parsing_errors = True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        response = search_agent.run(system_prompt + prompt, callbacks = [st_cb])
        #print(memory)
        st.session_state.messages.append({
            "role":"assistant",
            "content": response
        })
        st.write(response)

