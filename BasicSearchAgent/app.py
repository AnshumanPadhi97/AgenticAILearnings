from autogen.tools.experimental.tavily import TavilySearchTool
from autogen import AssistantAgent, LLMConfig
from dotenv import load_dotenv
import os

load_dotenv()

llm_config = LLMConfig(
    model="gemma3:4b",
    api_type="ollama",
    stream=False,
    client_host="http://localhost:11434",
)

assistant_agent = AssistantAgent(
    name="Ollama Assistant",
    llm_config=llm_config,
    system_message=(
        "You are an intelligent assistant that can perform web searches using the `tavily_search` tool. "
        "When you need to answer a question requiring current web information, use the tool by invoking it directly. "
        "You don't need to wrap the call in any code blocks or quotes; just invoke the function naturally, e.g., tavily_search('query'). "
        "Wait for the search results before generating your final answer. "
        "Be concise and accurate. End the conversation by saying 'terminate' when done."
    ),
    is_termination_msg=lambda msg: msg.get("content", "").strip().endswith("terminate"),
)

search_tool = TavilySearchTool(tavily_api_key=os.getenv("TAVILY_API_KEY"))
search_tool.register_tool(assistant_agent)

initial_prompt = (
    "You don’t know who the current Chief Minister of Odisha is. "
    "Use the tavily_search tool to find the most up-to-date information from the web."
)

response = assistant_agent.run(
    message=initial_prompt,
    max_turns=2
)

response.process()