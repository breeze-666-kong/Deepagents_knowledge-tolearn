from typing import TypedDict, Annotated

from langchain_core.messages import AIMessage

from langgraph.graph import add_messages, StateGraph,END
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent, CompiledSubAgent
import os

load_dotenv(find_dotenv())

llm= init_chat_model(
    model=os.getenv("LLM_QWEN_MAX"),
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

class SubState(TypedDict):
    messages:Annotated[list,add_messages]

def processing_node(state:SubState):
    print(f"调用了graph的子节点，传入的参数为：{state}")
    print("子节点的业务逻辑.....")
    return {"messages":[AIMessage(content=f"经过子节点处理后的结果！！原数据内容：{state['messages'][-1].content}")]}

workflow= StateGraph(SubState)
workflow.add_node("worker",processing_node)
workflow.set_entry_point("worker")
workflow.add_edge("worker",END)
compile_graph=workflow.compile()

sub_agent = CompiledSubAgent(
    name="graph_agent",
    description="处理所有的业务逻辑！！",
    runnable = compile_graph
)


main_agent= create_deep_agent(
    model=llm,
    tools=[],
    subagents=[sub_agent],
    system_prompt="你是一个指挥官，所有的业务动作，都需要使用graph_agent进行处理！"
)
stream= main_agent.stream({
    "messages":[{
        "role": "user",
        "content": "处理一段复杂业务，并核对id=1用户的数据是什么？"
    }
    ]
})

for chunk in stream:
    print(chunk)































