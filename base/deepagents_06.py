import os
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver  # 内存检查点，用于保存中断状态
from langgraph.types import Command  # 恢复执行的指令类型
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 1. 初始化模型
llm= init_chat_model(
    model=os.getenv("LLM_QWEN_MAX"),
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)
@tool
def delete_database(table_name: str):
    """
    高危动作工具，删除传入的表！
    :param table_name: 要删除的表名
    :return: 操作的返回结果
    """
    print(f"调用了删除了delete_database工具。删除了{table_name}表！！")
    return f"删除了表{table_name}！"

# 删除文件工具
@tool
def delete_file(file_name: str):
    """
    高危动作工具，删除传入的文件！
    :param file_name: 要删除的文件名
    :return: 操作的返回结果
    """
    print(f"调用了删除了delete_file工具。删除了{file_name}文件！！")
    return f"删除了文件{file_name}！"

# 查询表数据工具
@tool
def select_database(table_name: str):
    """
    查询动作工具，查询传入的表数据！
    :param table_name: 要查询的表名
    :return: 查询结果
    """
    print(f"调用了select_database工具。查询了{table_name}表数据！！")
    return f"查询了表{table_name}的数据！"

checkpointer= InMemorySaver()
thread_config={
    "configurable" :{"thread_id":"erdaye"}
}


main_agent= create_deep_agent(
    model=llm,
    tools=[delete_database,delete_file,select_database],
    subagents=[],
    system_prompt="回答使用中文，调用对应的工具实现对应的功能！",
    checkpointer=checkpointer,
    interrupt_on={
        "delete_database": True,  # 通过 编辑 或者拒绝 ,
        "delete_file": True,  # 通过 编辑 或者拒绝 ,  {"allowed_decisions": ["approve", "reject"]}
        "select_database": False
    }
)

#预执行
result_1= main_agent.invoke({
        "messages":[
        {"role":"user","content":"先查询product表的数据！再删除user表，最后，删除zhaoweifeng.txt文件"}
    ]
},config=thread_config)
#检查是否存在人机交互
interrupt= result_1["__interrupt__"]
if interrupt:
    action_requests = interrupt[0].value['action_requests']
    print(
        f"本次需要审核的工具数量：{len(action_requests)} ,具体拦截的工具：{[action['name'] for action in action_requests]}")
    decisions=[]
    for action in action_requests:
        action_name= action['name']
        action_args= action['args']
        if action_name=="delete_database":
            decisions.append({"type":"reject"})
            """
            类型为编辑代码如下:
            decisions.append({
               "type":"edit",
               "edited_action":{
                   # name -》 工具名
                   "name":action_name,
                   # args : { 修改的参数  key -> 参数名  value - > 修改的新的参数值 }
                   "args":{
                       "table_name":"hahahahahahahaherdaye"
                   }
               }
           })
            """
        elif action_name=="delete_file":
            decisions.append({"type": "approve"})
    #真正执行
    result_2 = main_agent.invoke(
            Command(
                resume={
                    "decisions": decisions
                }
            ),
            config=thread_config
        )
    print(f"最终结果{result_2['messages'][-1].content}")























