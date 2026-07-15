# 🤖 智扫通 — 扫地机器人 RAG 智能客服

基于 **LangChain ReAct Agent + Chroma 向量库 + 通义千问 qwen3-max** 构建的智能客服系统，支持产品咨询、故障排查、选购建议，并可根据用户使用数据生成个性化保养报告。

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-1C3C3C?logo=langchain)](https://www.langchain.com/)
[![Chroma](https://img.shields.io/badge/Chroma-向量数据库-FF6F61)](https://www.trychroma.com/)
[![Tongyi](https://img.shields.io/badge/LLM-通义千问_qwen3--max-orange)](https://tongyi.aliyun.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)

---

## 🎯 项目亮点

- ✅ **ReAct Agent 自主规划**：LLM 自主决策"思考→调用工具→观察→再思考"，非写死的 if-else 流程
- ✅ **RAG 检索增强生成**：5 个知识库文件（800+ 条 FAQ）→ Chroma 向量存储 → 语义检索 → 精准回答
- ✅ **动态提示词切换**：基于 Runtime Context 的中间件机制，通用问答/报告生成自动切换 System Prompt
- ✅ **中文优化分块**：分隔符列表加入中文标点（。！？），保证语义完整不截断
- ✅ **MD5 增量更新**：文件级哈希去重，重启只处理变更文件，节约 Embedding API 调用
- ✅ **三级可观测性**：工具调用监控 + 模型调用日志 + 控制台/文件双输出

---

## 🏗️ 技术栈

| 技术 | 选型 | 用途 |
|---|---|---|
| LLM 大模型 | 通义千问 qwen3-max | 对话推理、工具调用决策、答案生成 |
| Embedding 模型 | DashScope text-embedding-v4 | 文本转向量（1024 维），语义相似度检索 |
| Agent 框架 | LangChain `create_agent` | ReAct 模式编排，工具注册，中间件机制 |
| 向量数据库 | Chroma（本地持久化） | 嵌入式运行，零运维，适合中小规模知识库 |
| 文本分割 | `RecursiveCharacterTextSplitter` | 中文感知分层切分，chunk_size=200，overlap=20 |
| 文档加载 | PyPDFLoader + TextLoader | PDF 产品手册 + TXT FAQ 文件批量导入 |
| Web UI | Streamlit | 纯 Python 聊天界面，流式输出，会话管理 |
| 配置管理 | YAML | 4 个配置文件分离 LLM/Chroma/Prompts/Agent |
| 日志系统 | logging + TimedRotatingFileHandler | 按日滚动，控制台+文件双输出 |

---

## 📁 项目结构

```
Agent项目/
├── app.py                        # Streamlit 入口：聊天 UI、会话状态、流式渲染
├── agent/
│   ├── react_agent.py            # Agent 核心：create_agent 编排 + 动态提示词注入
│   └── tools/
│       ├── agent_tools.py        # 7 个工具函数（@tool 装饰器）
│       └── middleware.py          # 3 个中间件（工具监控、模型日志、动态提示词切换）
├── rag/
│   ├── vector_store.py           # Chroma 向量库：文档加载、中文分块、MD5 去重、嵌入存储
│   └── rag_service.py            # RAG 链路：检索 → 格式化上下文 → LLM 摘要 → 输出
├── model/
│   └── factory.py                # 抽象工厂：统一创建 LLM 和 Embedding 实例
├── utils/
│   ├── config_handler.py         # YAML 配置加载器
│   ├── file_handler.py           # PDF/TXT 加载、MD5 哈希、文件类型过滤
│   ├── logger_handler.py         # 日志系统（控制台 + 按日滚动）
│   ├── path_tool.py              # 项目根路径解析
│   └── prompt_loader.py          # 提示词文件加载器
├── config/
│   ├── rag.yml                   # LLM + Embedding 模型参数
│   ├── chroma.yml                # 向量库参数（chunk_size、k 值等）
│   ├── prompts.yml               # 提示词文件路径
│   └── agent.yml                 # 外部数据配置
├── prompts/
│   ├── main_prompt.txt           # 主系统提示词（角色 + 工具说明 + ReAct 规则）
│   ├── rag_summarize.txt         # RAG 摘要提示词（5 条严格约束）
│   └── report_prompt.txt         # 报告生成提示词（Markdown 格式规范）
└── data/
    ├── 扫地机器人100问2.txt       # 100 条通用 FAQ
    ├── 扫拖一体机器人100问.txt     # 100 条扫拖一体机型 FAQ
    ├── 故障排除.txt               # 200 条故障诊断（症状→诊断→修复）
    ├── 维护保养.txt               # 200 条维护指南（7 大类）
    ├── 选购指南.txt               # 200 条选购建议
    └── external/
        └── records.csv            # 模拟用户使用数据（10 用户 × 12 个月）
```

---

## 🧠 系统架构

```
┌──────────────────────────────────────────────────┐
│                 Streamlit Web UI                  │
│          (st.chat_message + 流式输出)              │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              ReAct Agent (LangChain)               │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  System Prompt · 动态切换                     │  │
│  │  main_prompt ←→ report_prompt                │  │
│  ├─────────────────────────────────────────────┤  │
│  │  7 Tools                                      │  │
│  │  ┌──────────────┐ ┌──────────────────────┐   │  │
│  │  │ rag_summarize │ │ get_user_id          │   │  │
│  │  │ get_product   │ │ get_current_month    │   │  │
│  │  │    _info      │ │ fill_context_for_    │   │  │
│  │  │ check_compat  │ │   report             │   │  │
│  │  │    _ibility   │ │ fetch_external_data  │   │  │
│  │  └──────────────┘ └──────────────────────┘   │  │
│  ├─────────────────────────────────────────────┤  │
│  │  3 Middleware                                 │  │
│  │  · monitor_tool · log_before_model           │  │
│  │  · report_prompt_switch (@dynamic_prompt)   │  │
│  └─────────────────────────────────────────────┘  │
└───────┬──────────────┬──────────────┬─────────────┘
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼───────────┐
│   Chroma     │ │  通义千问   │ │  外部数据       │
│   向量库      │ │  qwen3-max │ │  (records.csv) │
│  (本地持久化) │ │  (云端API)  │ │  (模拟后端)     │
└──────────────┘ └────────────┘ └────────────────┘
```

---

## 🔄 RAG 流程

### 文档摄取（离线）

```
data/ 目录 → 扫描 .txt / .pdf → MD5 哈希去重
  → PyPDFLoader / TextLoader 加载
  → RecursiveCharacterTextSplitter（中文标点感知，chunk=200）
  → DashScope text-embedding-v4 向量化（1024 维）
  → Chroma 持久化存储
```

### 检索增强生成（在线）

```
用户提问 → 向量化 Query → Chroma 语义检索 Top-3
  → 格式化上下文：参考资料1/2/3 + 元数据
  → Prompt 组装（系统提示词 + 上下文 + 用户问题）
  → 通义千问 qwen3-max 生成答案
  → StrOutputParser → 流式返回
```

---

## 💬 提示词工程

三套独立提示词模板，覆盖不同业务场景：

| 提示词 | 文件 | 场景 | 核心约束 |
|---|---|---|---|
| 主系统提示词 | `main_prompt.txt` | 通用问答 | ReAct 规则、工具说明、最多 5 次调用 |
| RAG 摘要提示词 | `rag_summarize.txt` | 知识检索 | **仅基于参考资料回答、禁止编造**、纯文本输出 |
| 报告生成提示词 | `report_prompt.txt` | 使用报告 | Markdown 格式、标题规范、保养建议 |

### 🔥 动态提示词切换（核心创新）

```
正常问答                    用户请求生成报告
    │                            │
    ▼                            ▼
main_prompt.txt           Agent 调用 fill_context_for_report
                              │
                         monitor_tool 中间件
                         context["report"] = True
                              │
                              ▼
                    @dynamic_prompt 中间件
                    下次 LLM 调用自动切换
                              │
                              ▼
                      report_prompt.txt
```

> 优势：无需用户手动切换模式，由工具调用链路自动触发，中间件实现关注点分离。

---

## 💾 向量库设计

### 选型：Chroma

| 对比维度 | Chroma（✅ 本项目） | FAISS | Milvus |
|---|---|---|---|
| 部署方式 | 嵌入式，零配置 | 嵌入式，需手动持久化 | 独立服务，Docker/K8s |
| 持久化 | ✅ 本地自动 | ❌ 需手动 save/load | ✅ |
| 元数据过滤 | ✅ | ❌ | ✅ |
| 规模上限 | 10 万级 | 百万级 | 十亿级 |
| 运维复杂度 | 极低 | 低 | 高 |

**选择理由**：知识库约 800 条 FAQ、向量总数 < 5000，Chroma 完全胜任；嵌入式运行零运维成本。

### 关键参数

| 参数 | 值 | 设计原因 |
|---|---|---|
| `chunk_size` | 200 字符 | 匹配单条 FAQ 长度，语义完整不碎片化 |
| `chunk_overlap` | 20 字符 | 10% 重叠，防止关键信息落在块边界 |
| `k`（检索数量） | 3 | FAQ 场景 1-2 个文档即可回答，k=3 留冗余 |
| 分隔符 | `\n\n→\n→。→！→？→空格` | 中文标点优先，在句子边界切分 |

---

## 🛠️ 7 个 Agent 工具

| 工具 | 说明 |
|---|---|
| `rag_summarize` | 从知识库检索相关文档并生成摘要回答 |
| `get_user_id` | 获取当前用户 ID（报告流程第 1 步） |
| `get_current_month` | 获取当前月份（报告流程第 2 步） |
| `fill_context_for_report` | **前置门禁**：填充报告上下文（第 3 步），触发动态提示词切换 |
| `fetch_external_data` | 拉取用户使用数据（第 4 步），基于 CSV 模拟后端 API |
| `get_product_info` | 获取产品参数信息 |
| `check_compatibility` | 检查配件兼容性 |

**报告生成严格序列**：`get_user_id → get_current_month → fill_context_for_report → fetch_external_data`，通过提示词硬约束 + 中间件验证双重保障。

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- 阿里云 DashScope API Key

### 1. 克隆项目

```bash
git clone git@github.com:ljz396929-ux/RAG.git
cd RAG
```

### 2. 安装依赖

```bash
pip install streamlit langchain langchain-chroma langchain-community \
            dashscope pypdf chromadb pyyaml
```

### 3. 配置 API Key

设置环境变量：

```bash
# Windows
set DASHSCOPE_API_KEY=你的API密钥

# macOS / Linux
export DASHSCOPE_API_KEY=你的API密钥
```

或在 `config/rag.yml` 中直接配置 API Key。

### 4. 初始化知识库

首次运行会自动扫描 `data/` 目录，加载所有 TXT/PDF 文件，切分并向量化存储到 Chroma。

### 5. 启动

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501`。

### 6. 开始对话

- 产品咨询："扫地机器人吸力不够怎么办？"
- 故障排查："机器不吸尘了，怎么排查？"
- 选购建议："家里有宠物，推荐哪款？"
- 生成报告："帮我生成本月的使用情况报告"

---

## 📊 知识库内容

| 文件 | 内容 | 条目数 |
|---|---|---|
| 扫地机器人100问2.txt | 基础使用、清洁效果、耗材维护、故障报警、高级功能、特殊场景 | 100 |
| 扫拖一体机器人100问.txt | 扫拖一体功能、拖地系统、清洁优化 | 100 |
| 故障排除.txt | 故障诊断（症状 → 诊断 → 修复）、200 项常见问题 | 200 |
| 维护保养.txt | 日常保养、扫地维护、拖地维护、耗材更换、环境适配、长期存放 | 200 |
| 选购指南.txt | 吸力、导航、避障、电池、水箱、集尘等选购要点 | 200 |

---

## 🔧 关键设计决策

### Agent 工具调用次数控制

LLM 可能陷入"调用→不满意→再调用"的无限循环。

**解决**：
- 提示词硬约束：最多 5 次工具调用
- LangChain `max_iterations` 参数兜底
- ReAct `Final Answer` 机制自动终止

### 中文文本分块

英文按空格/标点切分效果好，中文没有天然分词边界。

**解决**：
- 分隔符列表加入中文标点：`。！？`
- 优先在句子边界切分，小 chunk（200 字符）覆盖单条 FAQ

### 知识库增量更新

重启不应重新嵌入全部文档。

**解决**：
- 文件级 MD5 哈希去重
- `md5.txt` 记录已处理文件
- 只处理新增/变更文件

---

## 📝 生产环境升级建议

- [ ] **多路检索**：BM25 关键词 + 向量语义混合检索，引入 Cross-Encoder Reranker
- [ ] **向量库升级**：知识库超 10 万时迁移 Milvus / Pinecone
- [ ] **后端分离**：Streamlit → FastAPI + React/Vue，提升性能与定制能力
- [ ] **会话持久化**：对话历史存入数据库，支持跨设备同步
- [ ] **用户认证**：OAuth2.0 / SSO，区分用户权限和对话历史
- [ ] **可观测性**：接入 LangSmith / LangFuse，追踪 Token 消耗、延迟、工具链
- [ ] **多模型容灾**：主模型 qwen3-max + 备用模型，自动故障切换
- [ ] **相似问题缓存**：语义哈希缓存常见问题答案，减少 LLM 调用

---

## 📄 License

MIT License

---

*本项目是 LangChain + RAG 技术栈的学习实践，适合面试展示和 LLM 应用开发入门参考。*
