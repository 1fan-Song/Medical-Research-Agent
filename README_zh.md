# 🏥 Medical-Research-Agent

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://python.langchain.com/docs/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B)](https://streamlit.io/)

基于 **LangGraph** 构建的 Multi-Agent 医疗科研辅助智能体系统。

该系统旨在解决大模型在处理专业医学长文本时的“幻觉”与“溯源困难”问题。通过编排 8 个专业化的虚拟专家 Agent，实现从医学问题拆解、混合并发检索（PubMed 云端 + 本地 PDF 私有库），到最终生成**带有精确学术引用标记（如 `[1]`, `[2]`）**的 Markdown 医学综述报告。

## ✨ 核心架构与特性

- **🧠 Multi-Agent 状态机编排**：系统被解耦为 Planner（规划）、Retriever（检索）、Synthesizer（合成）、Quality Gate（质检）等多个节点，通过有向图（StateGraph）实现精准的流转与控制。
- **🔍 双擎混合检索 (Hybrid RAG)**：
  - **公有云知识**：集成 `BioPython` 直连 NCBI，抓取全球最新 PubMed 英文文献摘要。
  - **私有知识库**：集成 `PyMuPDF`，支持用户通过 Web 界面上传本地尚未发表的临床 PDF 数据，实现跨域知识融合。
- **🛡️ 零幻觉兜底与自动纠错**：
  - **自研 Citation Resolver**：强制大模型使用 `[DOC_xxx]` 标记事实来源，最终正则渲染为标准学术引用，确保 100% 来源可查。
  - **Quality Gate 质量闸门**：一旦发现初稿缺乏文献支撑或存在极高幻觉风险，系统将自动拦截并触发重试路由（打回重做）。
  - **空数据短路机制**：当面临极度前沿且无文献支撑的刁钻问题时，系统能优雅降级，主动声明“无直接证据”，拒绝捏造事实。
- **💻 现代化全栈交互**：基于 `Streamlit` 构建前端工作台，支持实时 Agent 思考节点追踪、Markdown 实时渲染与一键导出。

## 🚀 快速启动

### 1. 克隆项目
```bash
git clone https://github.com/1fan-Song/Medical-Research-Agent.git
cd Medical-Research-Agent
```
### 2. 环境配置与依赖安装

本项目推荐使用 **Conda** 进行环境隔离，已严格指定兼容的 Python 版本 (Python 3.10 - 3.13)。

**方式一：使用 Conda (推荐)**
```bash
conda env create -f environment.yml
conda activate medical-agent-env
```
方式二：使用 pip (需确保本地 Python >= 3.10)
```
bash
pip install -r requirements.txt
```
### 3. 环境配置
在项目根目录创建 .env 文件，并填入您的 API 配置（兼容任何支持 OpenAI 格式的大模型服务商）：
```ini
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=your_api_base_url_here
MODEL_NAME=your_model_name (e.g., gemini-2.5-flash)
```

### 4. 启动系统
```bash
streamlit run web_app.py
```
启动后，浏览器将自动打开 `http://localhost:8501`。 您可以在左侧边栏上传本地 PDF 文献，并在主界面输入医学科研问题开始检索。

### 📂 项目结构
```Plaintext
📦 Medical-Research-Agent
 ┣ 📂 agent                 # Agent 核心逻辑包
 ┃ ┣ 📂 nodes               # 8 大节点具体实现逻辑
 ┃ ┣ 📜 graph.py            # LangGraph 状态机路由编排
 ┃ ┣ 📜 prompts.py          # 提示词工程模板
 ┃ ┗ 📜 state.py            # 全局 State 数据结构定义
 ┣ 📂 papers                # 本地 PDF 私有知识库目录 (自动创建)
 ┣ 📜 web_app.py            # Streamlit 前端交互入口
 ┣ 📜 test_run.py           # 终端 CLI 测试入口
 ┣ 📜 requirements.txt      # 依赖清单
 ┗ 📜 .gitignore            # Git 忽略配置
```
### 👨‍💻 作者
Song Yifan (Shenzhen Institute of Advanced Technology / SUSTech)
