import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm_pick import pick_llm
from utils.etl_tools import ETLTools
from Models.schema import ETLAgentSchema, RouterSchema, DataAgentSchema
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.etl_analyst import etl_analyst
from agents.sql_analyst import sql_analyst

llm = pick_llm("medium")  # Pick the appropriate LLM based on the level of the question

llm_router = llm.with_structured_output(RouterSchema)  # Set the structured output schema for the LLM

# ------------------------------------  DATA AGENT GRAPH ------------------------------------

def router_node(state: DataAgentSchema):

    message = state.messages[-1].text  # Get the last message from the list of messages

    route_response_dict = llm_router.invoke(message).model_dump()

    route_response = route_response_dict['answer']  # Extract the answer from the structured output

    state.route_response = route_response

    return state

def etl_node(state: DataAgentSchema):

    message = state.messages[-1].text  # Get the last message from the list of messages

    response = etl_analyst.invoke(
             {"messages":[HumanMessage(content=f"""
            {message}
    """)]}
        ) 
    state.messages = state.messages + [response]

    return state

def sql_node(state: DataAgentSchema):

    message = state.messages[-1].text  # Get the last message from the list of messages

    input_schema = {
        "messages": [],
        "user_question": f"{message}",
        "curated_ques": "",
        "prompt_query_context": "",
        "generated_sql_query": "",
        "is_safe": "No",
        "comments": "",
        "sql_query_execution_result": "",
        "final_answer": ""
    }

    response = sql_analyst.invoke(input_schema)

    state.messages = state.messages + [response]

    return state

# -------------------------------------  DATA AGENT GRAPH ------------------------------------

# Nodes
data_agent_graph = StateGraph(DataAgentSchema)

data_agent_graph.add_node("router_node", router_node)
data_agent_graph.add_node("etl_node", etl_node)
data_agent_graph.add_node("sql_node", sql_node)

# Edges
data_agent_graph.add_edge(START, "router_node")

# Conditional Edges Function
def route_edge(state: DataAgentSchema) -> str:
    if state.route_response == "sql":
        return "sql_node"
    elif state.route_response == "etl":
        return "etl_node"
    else:
        raise ValueError(f"Invalid route response: {state.route_response}")

# -------------------------------------  Conditional Edges ------------------------------------
data_agent_graph.add_conditional_edges("router_node", route_edge,
                                      {
                                          "sql_node": "sql_node",
                                          "etl_node": "etl_node"
                                      })

# Compile the Graph
data_agent = data_agent_graph.compile()
