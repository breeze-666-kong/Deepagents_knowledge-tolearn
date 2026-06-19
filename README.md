# DeepAgents 学习笔记

DeepAgents 框架（v0.6.8）的个人学习记录，包含渐进式的代码 demo 和总结文档。

## 内容概览

| 文件 | 内容 |
|------|------|
| `deepagent_01.py` ~ `deepagent_02.py` | DeepAgent 入门：单智能体 + 网络搜索工具调用 |
| `deepagents_03.py` | 异步执行（async/await）和批量运行 |
| `deepagents_04.py` | 子智能体（SubAgent）+ `CompiledSubAgent`，LangGraph 节点集成 |
| `deepagents_05.py` | 多工具组合使用 |
| `deepagents_06.py` | HITL（人在回路）：`interrupt_on` 配置与人机交互审批流程 |
| `deepagents_07.py` ~ `deepagents_08.py` | 进阶用法 |
| `deepagents_09.py` | 长短期记忆：`CompositeBackend` 与 Store 持久化 |
| `deepagents_10.py` | 综合练习 |
| `deepagents_11.py` | Middleware（中间件）：`@wrap_tool_call` 自定义增强 |
| `deepagents_12.py` | 综合应用 |
| `DeepAgents使用总结.txt` | 个人总结文档，涵盖智能体创建、执行、子智能体、HITL、记忆、中间件、Skill 等 |

## 主要学习路径

1. **智能体创建** — `create_deep_agent(model, system_prompt, tools, subagents, ...)`
2. **执行方式** — 同步（invoke/stream）和异步（ainvoke/astream）
3. **子智能体** — 字典方式和 CompiledSubAgent 方式集成
4. **人在回路（HITL）** — interrupt_on + MemorySaver + Command(resume) 实现审批流程
5. **记忆系统** — 短期（MemorySaver）和长期（CompositeBackend / Store）
6. **中间件** — @wrap_tool_call 自定义工具调用前后处理
7. **Skill 系统** — 外置技能包加载机制
8. **兼容 LangGraph** — CompiledSubAgent 可直接包装 LangGraph 编译图
