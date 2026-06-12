from deepagents import create_deep_agent
from deepagents.backends import StoreBackend, StateBackend,FilesystemBackend,CompositeBackend
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
import os
load_dotenv(find_dotenv())

llm = init_chat_model(
    model=os.getenv("LLM_QWEN_MAX"),
    model_provider="openai"
)

store= InMemoryStore()

main_agent= create_deep_agent(
    model=llm,
    tools=[],
    backend=StoreBackend(),
    store=store,
    system_prompt="""
        你要把用户的重要信息保存到user_profile.txt文件中！
        获取用户信息可以读取user_profile.txt文件！
        """
)


config_a= {
    "configurable":{
        "thread_id":"a"
    }
}

config_b= {
    "configurable":{
        "thread_id":"b"
    }
}

result_a= main_agent.invoke(
    {
        "messages":[
            {"role":"user","content":"我是小明,17岁"}
        ]
    },
    config=config_a
)

print(f"第一次结果{result_a['messages'][-1].content}")
items = store.search(('filesystem',)) # ('filesystem',) -> 元组   ('filesystem' 不写, 变成字符串)
for item in items:
    print(f"key = {item.key}")
    print(f"value = {item.value}")

result_b= main_agent.invoke(
    {
        "messages":[
            {"role":"user","content":"我叫什么和年龄,可以读取user_profile.txt"}
        ]
    },
    config=config_b
)

print(f"回复结果{result_b['messages'][-1].content}")






































