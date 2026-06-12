import os
from pathlib import Path
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

llm= init_chat_model(
    model=os.getenv("LLM_QWEN_MAX"),
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

current_dir= Path(__file__).parent.resolve()
file_backend= FilesystemBackend(root_dir=current_dir, virtual_mode= True)

main_agent= create_deep_agent(
    model=llm,
    backend=file_backend,
    skills=[
        "skills"
    ],
    system_prompt="你一个智能助手，可以使用skill！"
)
query1 = "我早上起床晚了，赶公交车差点摔倒，还好最后到了公司！,使用emoji语言回答"
result = main_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": query1
            }
        ]
    }
)

print(f"最终输出结果：{result['messages'][-1].content}")


"""
  注意事项： 
     1. 先配置filebackend再配置skills属性  相对于file_backend的目录下 存储skill技能文件夹的名称
     2. skill的文件夹名称必须等于SKILL.md name = 名称
     3. SKILL渐进性加载，模型先加载SKILL元数据 yaml数据，根据需求再加载下面的提示词的md,元数据一定要清晰和简洁，必须有name和description
     4. 不是SKILL越多越好，7 - 10 ，多了模型也不会调用（摆烂），千万不要放重复功能的SKILL(选择苦难)
     5. 测试好 SKILL触发的提示词是什么！！
"""

























