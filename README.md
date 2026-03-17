# 🏥 Medical-Research-Agent

[**English**](./README.md) | [**中文说明**](./README_zh.md)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://python.langchain.com/docs/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B)](https://streamlit.io/)

A Multi-Agent medical research assistant system built on **LangGraph**.

This system is designed to tackle the critical challenges of "hallucinations" and "traceability" when Large Language Models (LLMs) process complex medical literature. By orchestrating a team of 8 specialized virtual AI agents, it seamlessly handles everything from medical query decomposition and concurrent hybrid retrieval (PubMed Cloud + Local PDF Vault) to synthesizing Markdown-formatted medical reviews with **precise academic citations (e.g., `[1]`, `[2]`)**.

## ✨ Core Architecture & Features

- **🧠 Multi-Agent Orchestration**: The system is decoupled into highly specialized nodes including Planner, Retriever, Synthesizer, and Quality Gate, controlled precisely via a directed graph (`StateGraph`).
- **🔍 Hybrid RAG (Retrieval-Augmented Generation)**:
  - **Public Cloud Knowledge**: Integrates `BioPython` to directly query NCBI, fetching the latest English abstracts from PubMed.
  - **Private Knowledge Vault**: Integrates `PyMuPDF`, allowing users to upload unpublished clinical PDF data via the Web UI for cross-domain knowledge fusion.
- **🛡️ Zero-Hallucination & Auto-Correction**:
  - **Citation Resolver Algorithm**: Forces the LLM to ground facts using `[DOC_xxx]` tags, which are strictly parsed into standard academic references, ensuring 100% traceability.
  - **Quality Gate**: Automatically intercepts drafts lacking literature support or exhibiting high hallucination risks, triggering a retry routing.
  - **Graceful Degradation**: When faced with highly specific queries lacking evidence, the system proactively declares "no direct evidence found" rather than fabricating facts.
- **💻 Modern Full-Stack UI**: A frontend workspace built with `Streamlit`, featuring real-time Agent thought-process tracking, live Markdown rendering, and one-click export.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/1fan-Song/Medical-Research-Agent.git](https://github.com/1fan-Song/Medical-Research-Agent.git)
cd Medical-Research-Agent
```

### 2. Environment Setup & Dependencies
This project recommends using Conda for environment isolation, strictly compatible with Python 3.10 - 3.13.

Option A: Using Conda (Recommended)

```bash
conda env create -f environment.yml
conda activate medical-agent-env
```
Option B: Using pip (Requires local Python >= 3.10)

```Bash
pip install -r requirements.txt
```
3. API Configuration
Create a .env file in the root directory and add your API credentials (compatible with any LLM provider supporting the OpenAI format):

```ini
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=your_api_base_url_here
MODEL_NAME=your_model_name (e.g., gemini-2.5-flash)
```
(Note: Ensure .env is included in your .gitignore to prevent secret leakage.)
### 4. Run the Application
```bash
streamlit run web_app.py
```
Upon launching, your browser will automatically open 'http://localhost:8501'. You can upload local PDF papers via the left sidebar and input your medical research queries in the main interface.

### 📂 Project Structure
```Plaintext
📦 Medical-Research-Agent
 ┣ 📂 agent                 # Core Multi-Agent logic
 ┃ ┣ 📂 nodes               # Implementations for the 8 Agent nodes
 ┃ ┣ 📜 graph.py            # LangGraph routing and orchestration
 ┃ ┣ 📜 prompts.py          # Prompt engineering templates
 ┃ ┗ 📜 state.py            # Global State data structure definition
 ┣ 📂 papers                # Private local PDF vault (Auto-created)
 ┣ 📜 web_app.py            # Streamlit frontend entry point
 ┣ 📜 test_run.py           # CLI testing entry point
 ┣ 📜 requirements.txt      # Python dependencies
 ┗ 📜 .gitignore            # Git ignore configurations
```
### 👨‍💻 Author
Song Yifan (Shenzhen Institute of Advanced Technology / SUSTech)
