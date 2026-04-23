from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from dotenv import load_dotenv
from typing import TypedDict, Annotated
load_dotenv()
model = ChatGroq(model="llama-3.1-8b-instant")


@tool
def mock_lead_capture(name: str, email: str, creater_platform: str):
    """
    Captures user lead information. 
    Args:
        name: The user's full name.
        email: The user's email address.
        creater_platform: The platform name (e.g., youtube, instagram).
    """
    return f"Captured lead: Name={name}, Email={email}, Platform={creater_platform}"

all_tools = [mock_lead_capture]
model_with_tools = model.bind_tools(all_tools)

class ChatState(TypedDict):
    history: Annotated[list[AnyMessage], add_messages]

def chat_node(state: ChatState):
    response = model_with_tools.invoke(state["history"])
    return {"history": [response]}

tools_node = ToolNode(all_tools, messages_key='history')


def custom_tools_condition(state: ChatState):
    last_message = state["history"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools_node"

    if "tool_calls" in getattr(last_message, "additional_kwargs", {}):
        return "tools_node"

    return "__end__"

def get_chatbot():
    load_dotenv()
    workflow = StateGraph(ChatState)
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("tools_node", tools_node)
    
    workflow.add_edge(START, "chat_node")
    workflow.add_conditional_edges("chat_node", custom_tools_condition)
    workflow.add_edge("tools_node", 'chat_node')
    return workflow.compile()