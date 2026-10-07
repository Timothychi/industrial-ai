# Industrial AI

基于 **Python + FastAPI + LLM + Agent + Tool + RAG + Milvus** 构建的工业制造领域 AI Agent 项目。

项目目标是构建一个面向工业制造场景的 **工艺知识 Agent**，帮助用户查询材料、理解加工工艺、检索企业知识，并在后续逐步扩展到设备、工艺参数、历史工艺、MES/ERP/WMS 等企业系统。

---

## 1. 项目定位

Industrial AI 当前以「**工艺知识 Agent**」作为第一阶段核心能力。

用户可以通过自然语言提出问题，例如：

```text
45号钢是什么材料？

45号钢车削时需要注意什么？

车削主要适用于哪些零件？

45号钢适合车削吗？
```

Agent 会根据问题自动判断是否需要调用工具：

```text
用户
 ↓
Process Agent
 ↓
LLM
 ↓
Function Calling
 ↓
Tool
 ├── Material Tool
 └── Knowledge Tool
       ↓
      RAG
       ↓
    Milvus
       ↓
   Reranker
       ↓
    Evidence
       ↓
      LLM
       ↓
    最终回答
```

项目重点不是简单地调用 LLM，而是探索：

* Agent 如何决策
* Tool 如何执行实际业务能力
* Function Calling 如何连接 LLM 和 Tool
* RAG 如何提供企业知识
* Metadata 如何增强工业知识检索
* Reranker 如何提升检索准确率
* Evidence 如何降低工业场景中的幻觉
* Memory 如何实现长期上下文记忆

---

# 2. 当前项目状态

目前已经完成第一阶段核心能力：

* [x] FastAPI API
* [x] LLM Client
* [x] Process Agent
* [x] Tool Registry
* [x] Function Calling
* [x] Material Tool
* [x] Knowledge Tool
* [x] Markdown 知识库
* [x] 文档 Loader
* [x] Markdown Splitter
* [x] Metadata
* [x] Embedding
* [x] Milvus 向量数据库
* [x] Vector Retriever
* [x] Reranker
* [x] 多 Tool 调用
* [x] Evidence / 知识依据
* [x] 基础防幻觉机制

后续计划：

* [ ] Conversation Memory
* [ ] Long-term Memory
* [ ] Equipment Tool
* [ ] Process Tool
* [ ] Historical Process Tool
* [ ] Hybrid Search
* [ ] PDF / Word / Excel Loader
* [ ] 知识库版本管理
* [ ] 多租户知识库
* [ ] Agent Workflow
* [ ] Multi-Agent
* [ ] MCP
* [ ] MES / ERP / WMS 集成
* [ ] 工业数据分析
* [ ] 工艺参数推荐
* [ ] Agent 监控与评估

---

# 3. 技术栈

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* httpx

## AI

* LLM
* Function Calling
* Agent
* Embedding
* RAG
* Reranker
* Sentence Transformers

## Vector Database

* Milvus

## Configuration

* python-dotenv
* `.env`

## Python Dependency Management

使用：

```bash
uv
```

管理 Python 项目和依赖。

---

# 4. 项目结构

当前项目结构：

```text
industrial-ai/
│
├── app/
│   │
│   ├── agent/
│   │   └── process_agent.py
│   │
│   ├── api/
│   │   └── chat.py
│   │
│   ├── llm/
│   │   └── client.py
│   │
│   ├── tools/
│   │   ├── knowledge.py
│   │   ├── material.py
│   │   └── registry.py
│   │
│   └── rag/
│       ├── embedding.py
│       ├── loader.py
│       ├── reranker.py
│       ├── retriever.py
│       ├── splitter.py
│       └── vector_store.py
│
├── knowledge/
│   └── turning.md
│
├── scripts/
│   └── ingest_knowledge.py
│
├── tests/
│   ├── test_embedding.py
│   └── test_retriever.py
│
├── .env
├── .gitignore
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 5. 核心模块说明

## 5.1 Agent

位置：

```text
app/agent/process_agent.py
```

`ProcessAgent` 是整个系统的核心编排层。

主要职责：

1. 接收用户问题
2. 将问题发送给 LLM
3. 根据 LLM 的 Function Calling 决定调用哪个 Tool
4. 执行 Tool
5. 将 Tool 结果返回给 LLM
6. 必要时继续调用其他 Tool
7. 最终生成答案

核心流程：

```text
User
 ↓
ProcessAgent
 ↓
LLM
 ↓
Tool Calling
 ↓
Execute Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

Agent 并不直接负责：

* 查询数据库
* 搜索 Milvus
* 查询材料
* 解析 PDF

这些能力应该由 Tool 提供。

---

# 6. Tool

位置：

```text
app/tools/
```

目前主要有两个 Tool。

## MaterialTool

```text
app/tools/material.py
```

负责查询材料基础信息。

例如：

```text
45号钢
铝合金
```

Tool：

```python
get_material(material_name)
```

返回：

```json
{
  "found": true,
  "data": {
    "name": "45号钢",
    "category": "中碳钢",
    "hardness": "HB170-220",
    "description": "常用中碳结构钢..."
  }
}
```

---

## KnowledgeTool

```text
app/tools/knowledge.py
```

负责搜索工业知识。

例如：

```text
45号钢车削需要注意什么？
```

内部调用：

```text
KnowledgeTool
    ↓
Retriever
    ↓
Embedding
    ↓
Milvus
    ↓
Reranker
    ↓
Evidence
```

---

# 7. Function Calling

项目通过 Function Calling 将 LLM 和 Tool 连接起来。

Tool 实际执行函数：

```python
TOOLS = {
    "get_material": get_material,
    "search_knowledge": search_knowledge,
}
```

同时向 LLM 提供 Tool Definition：

```python
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_material",
            "description": "查询工业材料的基本信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "material_name": {
                        "type": "string"
                    }
                },
                "required": [
                    "material_name"
                ]
            }
        }
    }
]
```

LLM 不直接执行 Python 函数。

而是产生结构化请求：

```text
LLM
 ↓
function call
 ↓
get_material
 ↓
Agent
 ↓
Python 函数
```

因此：

```text
Function Calling
```

本质上是：

> LLM 请求执行某个 Tool 的结构化协议。

而：

```text
Tool
```

是真正执行能力的代码。

---

# 8. RAG

RAG 是当前项目最重要的知识能力。

完整流程：

```text
知识文档
 ↓
Loader
 ↓
Splitter
 ↓
Metadata
 ↓
Embedding
 ↓
Milvus
```

查询：

```text
用户问题
 ↓
Embedding
 ↓
Milvus
 ↓
Top 20
 ↓
Reranker
 ↓
Top 5
 ↓
Evidence
 ↓
LLM
```

---

# 9. Knowledge Loader

位置：

```text
app/rag/loader.py
```

目前支持 Markdown。

例如：

```text
knowledge/turning.md
```

内容：

```markdown
# 车削工艺基础

## 1. 车削定义

车削是机械加工中常见的一种切削加工方法。

## 3. 45号钢车削

45号钢属于中碳钢...
```

Loader 负责：

```text
文件
 ↓
纯文本
```

后续计划支持：

```text
PDF
Word
Excel
Markdown
TXT
```

---

# 10. Document Splitter

位置：

```text
app/rag/splitter.py
```

当前采用 Markdown 章节和段落进行切分。

同时保留：

```text
title
section
source
```

例如：

```json
{
  "text": "45号钢属于中碳钢...",
  "source": "turning.md",
  "title": "车削工艺基础",
  "section": "45号钢车削"
}
```

相比简单地按照字符切割，这种方式能够保留知识上下文。

---

# 11. Metadata

工业知识库不能只有：

```text
text
```

还需要：

```text
source
title
section
material
process
page
version
```

例如：

```json
{
  "text": "45号钢车削时需要综合考虑...",
  "source": "机械加工工艺手册.pdf",
  "title": "车削工艺",
  "section": "45号钢车削",
  "material": "45号钢",
  "process": "车削",
  "page": 128,
  "version": "2026-01"
}
```

Metadata 的作用：

```text
语义检索
    +
结构化过滤
```

例如：

```text
material = 45号钢
process = 车削
```

然后再进行向量搜索。

这比单纯的 Vector Search 更适合工业知识库。

---

# 12. Embedding

位置：

```text
app/rag/embedding.py
```

负责：

```text
文本
 ↓
Embedding Model
 ↓
Vector
```

当前使用：

```text
BAAI/bge-small-zh-v1.5
```

例如：

```text
45号钢是什么材料？
```

转换成向量：

```text
[0.0123, -0.1823, ...]
```

然后存入 Milvus。

---

# 13. Milvus

位置：

```text
app/rag/vector_store.py
```

Milvus 用于保存和搜索向量。

当前 Collection：

```text
process_knowledge
```

核心字段：

```text
id
vector
text
source
title
section
material
process
```

搜索：

```text
query
 ↓
Embedding
 ↓
Vector
 ↓
Milvus
 ↓
Top K
```

当前使用：

```text
COSINE
```

作为向量相似度指标。

---

# 14. Retriever

位置：

```text
app/rag/retriever.py
```

Retriever 是 RAG 的检索核心。

当前流程：

```text
query
 ↓
Embedding
 ↓
Milvus Top 20
 ↓
Reranker
 ↓
Top 5
```

为什么先召回 20 个？

因为：

```text
Milvus
```

擅长：

> 快速找到可能相关的候选文档。

而不是：

> 精确判断哪个文档最适合当前问题。

因此需要：

```text
Milvus
 ↓
Recall
 ↓
Reranker
 ↓
Precision
```

---

# 15. Reranker

位置：

```text
app/rag/reranker.py
```

当前使用：

```text
BAAI/bge-reranker-base
```

Reranker 接收：

```text
Query
+
Document
```

然后重新计算相关性。

例如：

```text
Query:
45号钢车削需要注意什么？
```

候选：

```text
A：45号钢车削参数
B：铝合金车削
C：普通车削
D：45号钢材料性能
```

Reranker 会重新排序：

```text
A
D
C
B
```

最终只把 Top K 结果提供给 LLM。

---

# 16. Evidence

工业场景不能简单依赖 LLM 自己的知识。

项目采用：

```text
Knowledge Retrieval
 ↓
Evidence
 ↓
LLM
```

Evidence 包含：

```json
{
  "text": "...",
  "source": "turning.md",
  "title": "车削工艺基础",
  "section": "45号钢车削",
  "material": "45号钢",
  "process": "车削",
  "rerank_score": 0.91
}
```

Agent 应该遵循：

> 能从知识库找到依据，就基于知识库回答。

如果没有足够依据：

> 明确告诉用户当前知识库没有足够依据。

而不是自行编造具体工业参数。

---

# 17. 防止工业知识幻觉

项目重点遵循：

```text
知识库有依据
    ↓
基于 Evidence 回答

知识库没有依据
    ↓
明确说明无法确认

不能
    ↓
使用 LLM 常识编造工业参数
```

例如：

```text
用户：

316L 不锈钢激光焊接推荐功率是多少？
```

如果知识库没有相关数据：

```text
当前知识库没有找到足够依据，
无法可靠给出具体激光功率参数。
```

而不是：

```text
推荐 3000W。
```

工业场景中，这一点非常重要。

---

# 18. LLM Client

位置：

```text
app/llm/client.py
```

负责统一封装 LLM API。

Agent 不直接处理：

```text
httpx
HTTP Header
API URL
API Key
```

而是：

```python
llm.chat(...)
```

这样以后可以方便切换不同模型服务。

整体关系：

```text
ProcessAgent
      ↓
  LLMClient
      ↓
   LLM API
```

---

# 19. API

入口：

```text
main.py
```

Chat API：

```text
app/api/chat.py
```

当前接口：

```http
POST /chat
```

请求：

```json
{
  "message": "45号钢车削时需要注意什么？"
}
```

返回：

```json
{
  "message": "..."
}
```

---

# 20. 启动项目

## 安装依赖

项目使用 `uv`。

如果还没有安装：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

然后：

```bash
uv sync
```

---

# 21. 配置环境变量

创建：

```text
.env
```

例如：

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-llm-service/v1
LLM_MODEL=your-model
```

不要把真实 API Key 提交到 Git。

建议 `.gitignore`：

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
```

---

# 22. 启动 FastAPI

```bash
uv run uvicorn main:app --reload
```

默认：

```text
http://127.0.0.1:8000
```

Swagger：

```text
http://127.0.0.1:8000/docs
```

---

# 23. 启动 Milvus

项目需要先启动 Milvus。

默认连接：

```text
http://localhost:19530
```

确保 Milvus 正常运行后，再进行知识入库。

---

# 24. 知识入库

当前知识文档：

```text
knowledge/turning.md
```

执行：

```bash
uv run python scripts/ingest_knowledge.py
```

完整流程：

```text
turning.md
    ↓
Loader
    ↓
Splitter
    ↓
Metadata
    ↓
Embedding
    ↓
Milvus
```

---

# 25. 测试 Embedding

```bash
uv run python -m app.tests.test_embedding
```

测试：

* Embedding 模型是否正常
* 向量维度
* Embedding 是否能够正常生成

---

# 26. 测试 Retriever

```bash
uv run python -m app.tests.test_retriever
```

例如：

```text
查询：

45号钢车削需要注意什么？
```

查看：

```text
向量分数
Rerank 分数
材料
工艺
章节
知识内容
```

---

# 27. 测试 Agent

启动：

```bash
uv run uvicorn main:app --reload
```

请求：

```bash
curl -X POST \
  http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "45号钢车削时需要注意什么？"
  }'
```

Agent 预期执行：

```text
User
 ↓
ProcessAgent
 ↓
LLM
 ↓
search_knowledge
 ↓
Retriever
 ↓
Milvus
 ↓
Reranker
 ↓
Evidence
 ↓
LLM
 ↓
Answer
```

---

# 28. 多 Tool Agent

当前 Agent 支持多个 Tool。

例如：

```text
用户：

45号钢适合车削吗？
车削时需要注意什么？
```

Agent 可以根据问题调用：

```text
get_material("45号钢")

+

search_knowledge("45号钢车削注意事项")
```

然后：

```text
MaterialTool Result
        +
KnowledgeTool Result
        ↓
       LLM
        ↓
   综合回答
```

这也是项目从：

```text
Chatbot
```

向：

```text
Agent
```

转变的关键。

---

# 29. Agent 的核心循环

当前 Agent 本质上是：

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason
  ↓
Act
  ↓
Observe
  ↓
Final Answer
```

代码层面对应：

```python
while True:

    response = await llm.chat(...)

    if no_tool_call:
        return answer

    execute_tools()

    append_tool_result()

    continue
```

因此 Agent 并不是简单：

```text
LLM + Prompt
```

而是：

```text
Agent
=
LLM
+
Tools
+
Function Calling
+
Execution Loop
+
State
```

---

# 30. 后续架构规划

项目后续计划逐步演进为：

```text
                           Industrial AI
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
              Agent                         RAG
                 │                             │
        ┌────────┼────────┐           ┌────────┼────────┐
        │        │        │           │        │        │
   Material  Equipment  Process    Loader  Retriever Reranker
      Tool      Tool      Tool        │        │        │
                                      ↓        ↓        ↓
                                   Documents Milvus Evidence
```

进一步：

```text
                    Process Agent
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
 KnowledgeTool       MaterialTool      EquipmentTool
       │                  │                  │
      RAG               Material DB       Equipment DB
       │
    Evidence
```

最终扩展到：

```text
                         Industrial AI
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Agent            RAG             Memory
             │                │                │
          Tools          Knowledge         Short-term
             │            Base             Long-term
             │                               │
      ┌──────┼──────┐                        │
      │      │      │                        │
    MES    ERP    WMS                 Memory Store
```

---

# 31. Roadmap

## Phase 1：Agent 基础

* [x] FastAPI
* [x] LLM Client
* [x] Agent
* [x] Tool
* [x] Function Calling
* [x] Multi Tool

## Phase 2：RAG

* [x] Document Loader
* [x] Document Splitter
* [x] Metadata
* [x] Embedding
* [x] Milvus
* [x] Retriever
* [x] Reranker
* [x] Evidence

## Phase 3：Memory

* [ ] Conversation Memory
* [ ] Short-term Memory
* [ ] Long-term Memory
* [ ] Memory Retrieval
* [ ] User Profile Memory
* [ ] Equipment Memory
* [ ] Process Memory

## Phase 4：工业 Tool

* [ ] Material Tool
* [ ] Equipment Tool
* [ ] Process Tool
* [ ] Historical Process Tool
* [ ] Production Data Tool
* [ ] Quality Data Tool

## Phase 5：企业系统

* [ ] MES
* [ ] ERP
* [ ] WMS
* [ ] PLM
* [ ] QMS

## Phase 6：Agent Workflow

* [ ] Workflow
* [ ] Planning
* [ ] Human-in-the-loop
* [ ] Approval
* [ ] Task Execution
* [ ] Retry
* [ ] Error Recovery

## Phase 7：Multi-Agent

规划：

```text
                    Supervisor Agent
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
       Process Agent   Equipment Agent   Quality Agent
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                      Final Answer
```

## Phase 8：MCP / A2A

后续研究：

```text
MCP
 ↓
标准化 Tool / Resource 接入
```

以及：

```text
A2A
 ↓
Agent ↔ Agent
```

---

# 32. 项目最终目标

最终希望构建的不是一个简单的：

```text
工业 ChatGPT
```

而是一个可以真正参与工业业务流程的：

```text
Industrial AI Agent
```

例如：

```text
用户：

帮我分析一下45号钢这个零件的车削工艺，
结合当前设备能力和历史加工记录，
给出工艺建议。
```

Agent 可以：

```text
                    Agent
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
      Material     Knowledge   Equipment
        Tool          RAG         Tool
          │           │           │
          ↓           ↓           ↓
       材料信息     工艺知识     设备能力
          │           │           │
          └───────────┼───────────┘
                      ↓
               Historical Data
                      ↓
                    Agent
                      ↓
                工艺分析建议
                      ↓
                人工确认/审批
                      ↓
                执行企业流程
```

最终形成：

```text
Knowledge
+
Reasoning
+
Tools
+
Memory
+
Workflow
+
Enterprise Systems
```

这才是 Industrial AI Agent 的完整方向。

---

# 33. 学习目标

这个项目同时用于学习以下 AI 工程核心概念：

```text
LLM
 │
 ├── Token
 ├── Prompt
 ├── Context
 │
 ├── Function Calling
 │
 ├── Tool
 │
 ├── Agent
 │
 ├── RAG
 │    ├── Loader
 │    ├── Splitter
 │    ├── Embedding
 │    ├── Vector DB
 │    └── Reranker
 │
 ├── Memory
 │
 ├── Workflow
 │
 ├── MCP
 │
 └── A2A
```

项目采用**逐步实现、逐步验证**的方式，而不是一次性引入完整 Agent Framework。

这样可以先理解每一个核心组件的原理，再考虑使用 LangChain、LlamaIndex、LangGraph 等框架进行工程化封装。
