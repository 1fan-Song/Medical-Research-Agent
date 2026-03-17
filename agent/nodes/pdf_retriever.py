# agent/nodes/pdf_retriever.py

import os
import fitz  # PyMuPDF
from agent.state import ResearchState

def pdf_retriever_node(state: ResearchState) -> dict:
    print("\n--- 📂 节点运转中：[Node 3] PDF Retriever 检索本地文档 ---")
    
    # 设定本地私有文献库的文件夹
    folder_path = "./papers"
    
    # 如果文件夹不存在，自动创建并直接返回
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"    ⚠️ 未找到本地 {folder_path} 文件夹。已自动创建，请在未来放入 PDF 文献。")
        return {"raw_evidence": []}

    local_evidence = []
    
    # 从规划器提取检索关键词 (简化处理，取前两个 query 里的长单词)
    queries = state.get("search_queries", [])
    keywords = [w.strip('()""') for q in queries for w in q.split() if len(w) > 5]
    
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"    📂 {folder_path} 文件夹为空，跳过本地检索。")
        return {"raw_evidence": []}

    print(f"    📖 正在翻阅本地 {len(pdf_files)} 篇 PDF 文献...")
    
    for file in pdf_files:
        try:
            doc = fitz.open(os.path.join(folder_path, file))
            # 为了速度，只扫描每篇文献的前 5 页（通常包含摘要和引言）
            text = "".join([page.get_text() for page in doc[:5]])
            
            # 如果本地文献的文本里命中了我们的核心关键词，就抓取出来
            if any(kw.lower() in text.lower() for kw in keywords[:10]):
                local_evidence.append({
                    "source": f"本地私有库: {file}",
                    "content": text[:3000] # 截取前 3000 字符
                })
            doc.close()
        except Exception as e:
            print(f"    ❌ 读取文件 {file} 时出错: {e}")

    print(f"    ✅ 本地 PDF 检索完成，挖掘到 {len(local_evidence)} 条相关证据。")
    
    # 💡 注意：这里使用 raw_evidence，它会和 PubMed 的结果自动合并 (并行写入)
    return {"raw_evidence": local_evidence}