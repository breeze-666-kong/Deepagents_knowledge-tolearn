import os
from langchain_core.tools import tool
from typing import Literal
from tavily import TavilyClient
from dotenv import load_dotenv,find_dotenv
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
#读取环境
load_dotenv (find_dotenv())


llm_name= os.getenv("LLM_QWEN_MAX")
tavily_key= os.getenv("TAVILY_API_KEY")

tavily_client= TavilyClient(api_key=tavily_key)

#初始化大模型
llm= init_chat_model(
    model= llm_name,
    model_provider= "openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
@tool
def internet_search(query: str,max_results: int = 5,topic:Literal["news", "finance", "general"] = "general",include_raw_content:bool = False) -> str:
    """
    Search for information using Tavily.
    """
    print(f"开始搜索,参数:{query},{max_results},{topic},{include_raw_content}")


    return tavily_client.search(query=query,max_results=max_results,topic=topic,include_raw_content=include_raw_content)

deep_agent= create_deep_agent(model=llm,
                tools=[internet_search],
                subagents= [],
                system_prompt= """
                你是一个专家级的研究员！你有权使用工具：internet_search网络信息！
                最终，需要你根据收集工具，生成一份精美的报告！
                """  )

stream= deep_agent.stream(
    {
        "messages":[
            {
                "role": "user","content":"查询人工智能和机器人的热门新闻信息"
            }
        ]
    }
)
for chunk in stream:
    for node_name,state in chunk.items():
        if not state or "messages" not in state:
            continue
        messages= state["messages"]
        if messages and isinstance(messages,list):
            last_msg = messages[-1]
            if node_name == "model":
                #三种可能:返回结果,使用子智能体,决定调用哪种工具
                if last_msg.tool_calls:
                    for tool_call in last_msg.tool_calls:
                        if tool_call["name"]=="task":
                            print(f"调用子智能体{tool_call['args']['subagent_type']}")
                        else:
                            print(f"调用工具{tool_call['name']},传入参数:{tool_call['args']}/n")
                elif last_msg.content:
                    print(f"返回结果:{last_msg.content}")
            if node_name == "tools":
                #一种可能:调用工具
                tool_return = last_msg.content[:100]+"........."
                tool_name= last_msg.name
                print(f"使用工具{tool_name}，返回结果:{tool_return}")


























