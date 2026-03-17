# web_app.py

import streamlit as st
import time
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv() 

from agent.graph import build_graph

# 1. 页面全局配置
st.set_page_config(
    page_title="Medical Research Agent",
    page_icon="🏥",
    layout="wide"
)

# 确保本地文献库文件夹存在
PAPERS_DIR = "./papers"
if not os.path.exists(PAPERS_DIR):
    os.makedirs(PAPERS_DIR)

# 2. 侧边栏信息与 PDF 上传功能
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/microscope.png", width=60)
    st.title("系统面板")
    st.markdown("""
    **核心架构：**
    - 🧠 Multi-Agent 协作网络
    - 🔍 BioPython 官方直连检索
    - 📂 本地 PDF 私有库解析
    - 🛡️ 防幻觉质量闸门 (Quality Gate)
    """)
    
    st.divider()
    
    # 💡 新增功能：PDF 私有库上传
    st.subheader("📁 私有文献库构建")
    st.caption("上传的 PDF 将自动加入 Agent 的本地检索池")
    
    # 支持多文件上传
    uploaded_files = st.file_uploader("拖拽或点击上传 PDF", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        save_count = 0
        for uploaded_file in uploaded_files:
            file_path = os.path.join(PAPERS_DIR, uploaded_file.name)
            # 避免重复保存同一个文件消耗性能
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                save_count += 1
                
        if save_count > 0:
            st.success(f"✅ 成功将 {save_count} 篇新文献存入本地知识库！")
        else:
            st.info("文件已存在于本地知识库中。")

    st.divider()
    st.caption("Powered by LangGraph & Gemini")

# 3. 主界面 UI
st.title("🏥 智能医疗科研助手")
st.markdown("输入您的临床或医学科研问题，Agent 团队将综合 **PubMed 云端** 与 **本地 PDF 私有库**，自动生成包含精确溯源的学术综述报告。")

query = st.text_area(
    "🔬 请输入科研问题：",
    value="TP53基因突变对非小细胞肺癌（NSCLC）患者使用PD-1抑制剂的疗效有什么影响？",
    height=100
)

# 4. 核心执行逻辑
if st.button("🚀 启动深度检索与生成", type="primary"):
    if not query.strip():
        st.warning("问题不能为空哦！")
    else:
        with st.status("🤖 Agent 团队正在火速运转中 (预计耗时 1-2 分钟)...", expanded=True) as status:
            try:
                app = build_graph()
                initial_state = {"research_question": query}
                final_report = ""
                
                for output in app.stream(initial_state):
                    for node_name, node_state in output.items():
                        st.write(f"✅ **[{node_name}]** 节点执行完毕")
                        if "final_report" in node_state:
                            final_report = node_state["final_report"]
                            
                status.update(label="🎉 综述报告生成完毕！", state="complete", expanded=False)
                
                # 5. 渲染最终的 Markdown 报告
                st.divider()
                st.subheader("📝 最终生成的医学综述")
                st.markdown(final_report)
                
                st.download_button(
                    label="⬇️ 下载 Markdown 报告",
                    data=final_report,
                    file_name=f"Medical_Report_{int(time.time())}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                status.update(label="🚨 系统运行出错", state="error", expanded=True)
                st.error(f"发生异常: {e}")