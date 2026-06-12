import asyncio

from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
import os

load_dotenv(find_dotenv())

llm= init_chat_model(
    model=os.getenv("LLM_QWEN_MAX"),
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

weather_agent={
    "name": "weather_agent",
    "description": "用于查询天气信息智能助手，当用户询问查询天气的时候，调用此助手完成任务！",
    "system_prompt":"你是一个天气查询助手，无论用户查询哪个城市，你统一回复：'今天天气晴朗，温度25度！'",
    "tools":[]
}


math_agent={
    "name": "math_agent",
    "description": "用于计算！",
    "system_prompt":"你是一个严谨的数学助手，帮助用户回答计算算数等问题'",
    "tools":[]
}

translate_agent={
    "name": "translate_agent",
    "description": "用于翻译！",
    "system_prompt":"你是一个严谨的翻译助手，帮助用户翻译语言'",
    "tools":[]
}

main_agent= create_deep_agent(
    model=llm,
    tools=[],
    subagents=[weather_agent,math_agent,translate_agent],
    system_prompt="你是一个管理者,用于管理何时调用其他智能体回答问题,不可自己直接回答问题！"
)


async def test(query):
    stream= main_agent.astream(
        {
            "messages":[
                {
                    "role": "user","content":query
                }
            ]
        }
    )
    async for chunk in stream:
        for node_name,state in chunk.items():
            if not state or "messages" not in state:continue
            messages= state["messages"]
            if messages and isinstance(messages,list):
                last_msg = messages[-1]
                if node_name == "model":
                    if last_msg.tool_calls:
                        for tool_call in last_msg.tool_calls:
                            if tool_call["name"]=="task":
                                print(f"调用子智能体{tool_call['args']['subagent_type']}")
                            else:
                                print(f"调用工具{tool_call['name']},传入参数:{tool_call['args']}/n")
                    if last_msg.content:
                        print(f"返回最终结果:{last_msg.content}")
                elif node_name=="tools":
                    name= last_msg.name
                    tool_return = last_msg.content[:100]+"........."
                    print(f"使用工具{name}，返回结果:{tool_return}")



if __name__ == "__main__":
    async def batch_run():
        # 要执行的并发协程对象获取到
        tast1 = test("北京今天的天气怎么样？")
        tast2 = test("请将'我要上楼打他'翻译成英文！")
        print(type(tast1))
        print(type(tast2))
        await asyncio.gather(tast1,tast2)

    asyncio.run(batch_run())













