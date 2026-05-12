# 论文评估系统 API（RAG + FastAPI）

基于 **RAG（检索增强生成）** 与 **FastAPI** 构建的轻量级论文问答系统。

系统会自动加载本地论文文本，通过向量检索召回相关内容，再结合大语言模型生成回答，实现：

> 上传文档 → 向量检索 → 智能问答

的完整闭环。

---

# ✨ 功能特点

- 自动读取 `papers/` 文件夹中的 `.txt` 文件
- 自动切分文本并构建 Chroma 向量数据库
- 提供 `/query` API 接口实现论文问答
- 使用本地大模型（Ollama + Qwen2.5）推理
- 数据本地运行，不依赖外部 API
- 自动生成 Swagger API 测试页面

---

# 📦 技术栈

| 模块 | 工具 / 框架 |
|------|-------------|
| Web 框架 | FastAPI、Uvicorn |
| RAG 流程 | LangChain + LCEL |
| 向量数据库 | Chroma |
| 嵌入模型 | sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`) |
| 本地大模型 | Ollama + Qwen2.5:7b |
| 文本处理 | langchain-text-splitters、langchain-community |

---

# 📁 项目结构

```bash
rag-paper-eval/
│
├── papers/              # 存放论文 txt 文件
├── main.py              # FastAPI 主程序
├── requirements.txt     # 项目依赖
└── README.md
```

---

# 🚀 快速开始

## 1. 克隆仓库

```bash
git clone https://github.com/yourusername/rag-paper-eval.git
cd rag-paper-eval
```

---

## 2. 创建虚拟环境

### Windows（PowerShell）

```bash
python -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. 安装依赖

```bash
pip install --upgrade pip

pip install fastapi uvicorn \
langchain langchain-community langchain-core \
chromadb sentence-transformers \
langchain-text-splitters
```

---

## 4. 安装并启动 Ollama

先从官方下载安装：

- https://ollama.com

安装完成后，拉取推荐模型：

```bash
ollama pull qwen2.5:7b
```

> 首次下载约 4~5 GB。

确保 Ollama 服务已启动（一般安装后会自动运行）。

---

## 5. 准备论文文档

在项目根目录创建：

```bash
papers/
```

将需要问答的 `.txt` 文件放入其中。

示例：

```bash
papers/
├── transformer.txt
├── bert.txt
└── rag.txt
```

推荐使用 UTF-8 编码。

---

## 6. 启动服务

```bash
uvicorn main:app --reload
```

如果终端出现：

```bash
Application startup complete.
```

说明服务启动成功。

---

# 📖 API 使用

## 接口信息

| 项目 | 内容 |
|------|------|
| URL | `http://127.0.0.1:8000/query` |
| 方法 | `POST` |
| 数据格式 | `application/json` |

---

## 请求示例

```json
{
  "query": "什么是注意力机制？"
}
```

---

## 响应示例

```json
{
  "answer": "注意力机制是 Transformer 模型的核心，它允许模型在处理序列时动态关注不同位置的信息。"
}
```

---

# 🧪 在线测试

启动服务后访问：

```text
http://127.0.0.1:8000/docs
```

即可使用 FastAPI 自动生成的 Swagger UI 进行接口测试。

---

# 🧠 系统工作流程

```text
用户问题
   ↓
向量检索（Chroma）
   ↓
召回相关论文片段
   ↓
LLM（Qwen2.5）
   ↓
生成最终回答
```

---

# 🔮 后续开发方向

- 支持 PDF / DOCX 文档解析
- 多模态论文解析（图片、公式）
- 引文自动校验
- MCP 工具调用
- Agent 化论文评估
- Web 前端页面
- 用户上传文档功能
- 多用户数据库隔离

---

# 📜 License

MIT License