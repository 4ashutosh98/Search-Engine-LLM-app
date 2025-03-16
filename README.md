---
title: Search Engine LLM App
emoji: 🌍
colorFrom: pink
colorTo: indigo
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
license: mit
short_description: This app allows you to chat with an LLM that can search web.
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Search Engine LLM App

## Overview
This application is a powerful research assistant built with Langchain that can search across multiple knowledge sources including Wikipedia, arXiv, and the web via DuckDuckGo. It leverages Groq's LLM capabilities to provide intelligent, context-aware responses to user queries.

## Live Demo
Try the application live at: [Hugging Face Spaces](https://huggingface.co/spaces/ashutoshchoudhari/Search-Engine-LLM-app)

## Features
- **Multi-source search**: Access information from Wikipedia, arXiv scientific papers, and web results
- **Conversational memory**: Retains context from previous interactions
- **Streaming responses**: See the AI's response generated in real-time
- **User-friendly interface**: Clean Streamlit UI for easy interaction

## Technical Components
- **LLM**: Groq's Llama3-8b-8192 model (with fallback support for Ollama models)
- **Embeddings**: Hugging Face's all-MiniLM-L6-v2
- **Search Tools**:
  - Wikipedia API
  - arXiv API
  - DuckDuckGo Search
- **Framework**: Langchain for agent orchestration
- **Frontend**: Streamlit

## Project Structure
- **app.py**: Main application file containing the Streamlit UI and Langchain integration
- **requirements.txt**: Dependencies required to run the application
- **README.md**: Project metadata and description for Hugging Face Spaces
- **tools_agents.ipynb**: Jupyter notebook demonstrating how to use Langchain tools and agents
- **.github/workflows/main.yaml**: GitHub Actions workflow for deploying to Hugging Face Spaces
- **.gitattributes**: Git LFS configuration for handling large files
- **.gitignore**: Standard Python gitignore file
- **LICENSE**: MIT License file
- **app_documentation.md**: This comprehensive documentation file

## Implementation Details

### LLM Integration
The application uses Groq's API to access the Llama3-8b-8192 model with streaming capability:

```python
llm = ChatGroq(
    groq_api_key = st.session_state.api_key, 
    model_name = "Llama3-8b-8192", 
    streaming = True
)
```

Alternative local models can also be configured with Ollama:
```python
#llm = ChatOllama(base_url=OLLAMA_WSL_IP, model="llama3.1", streaming=True)
```

### Search Tools Configuration
The app configures three primary search tools:

1. **Wikipedia Search**:
```python
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results = 3, doc_content_chars_max=10000)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
wiki_tool= Tool(
    name = "Wikipedia",
    func = wiki.run,
    description = "This tool uses the Wikipedia API to search for a topic."
)
```

2. **arXiv Search**:
```python
api_wrapper_arxiv = ArxivAPIWrapper(top_k_results = 5, doc_content_chars_max=10000)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
arxiv_tool = Tool(
    name = "arxiv",
    func = arxiv.run,
    description = "Searches arXiv for papers matching the query.",
)
```

3. **DuckDuckGo Web Search**:
```python
api_wrapper_ddg = DuckDuckGoSearchAPIWrapper(region="us-en", time="y", max_results=10)
ddg = DuckDuckGoSearchResults(
    api_wrapper=api_wrapper_ddg,
    output_format="string",
    handle_tool_error=True,
    handle_validation_error=True)
ddg_tool = Tool(
    name = "DuckDuckGo_Search",
    func = ddg.run,
    description = "Searches for search queries using the DuckDuckGo Search engine."
)
```

### Agent Configuration
The system uses the CHAT_CONVERSATIONAL_REACT_DESCRIPTION agent type with a conversational memory buffer:

```python
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

search_agent = initialize_agent(
    tools = tools,
    llm = llm,
    agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    max_iterations = 10,
    memory = memory,
    handle_parsing_errors = True)
```

## Setup Requirements
1. Groq API key
2. Hugging Face token (for embeddings)
3. Python environment with required dependencies

## Installation Instructions
Install the required packages using:

```bash
pip install -r requirements.txt
```

Required packages include:
- arxiv
- wikipedia
- langchain, langchain-community, langchain-huggingface, langchain-groq
- openai
- duckduckgo-search
- ollama, langchain-ollama (for local model support)

## Environment Variables
Create a `.env` file with the following variables:
```
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

## Usage
1. Start the application using Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Enter your Groq API key in the sidebar when prompted
3. Type your research question in the chat input box
4. The agent will search across available sources and provide a comprehensive response
5. Your conversation history will be maintained throughout the session

## Example Queries
- "What are the latest developments in quantum computing?"
- "Explain the concept of transformer models in NLP"
- "What were the key findings from the recent climate change report?"
- "Tell me about the history and applications of reinforcement learning"

## Deployment
This project is configured to deploy to Hugging Face Spaces using GitHub Actions. The workflow in `.github/workflows/main.yaml` automatically syncs the repository to Hugging Face when changes are pushed to the main branch.

### Live Application
The app is currently deployed and accessible at: [Hugging Face Spaces](https://huggingface.co/spaces/ashutoshchoudhari/Search-Engine-LLM-app)

### Local Development
For local development, you can use:
```bash
streamlit run app.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Langchain for providing the agent and tool framework
- Groq for the LLM API access
- Hugging Face for embeddings and hosting capabilities

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.