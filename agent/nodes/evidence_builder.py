# agent/nodes/evidence_builder.py

from agent.state import ResearchState

def evidence_builder_node(state: ResearchState) -> dict:
    print("\n--- 🧱 节点运转中：[Evidence Builder] 构建结构化证据库 ---")
    
    # 从状态机黑板上取下 PubMed 和 PDF 并行抓回来的所有原始数据
    raw_evidence = state.get("raw_evidence", [])
    
    if not raw_evidence:
        print("    ⚠️ 未收到任何原始证据。")
        return {"structured_evidence": []}

    structured_evidence = []
    print(f"    📥 正在清洗和结构化 {len(raw_evidence)} 条原始数据...")

    # 遍历所有证据，强行注入全局唯一的 doc_id
    for i, ev in enumerate(raw_evidence):
        # 生成标准化条形码，例如：DOC_001, DOC_002
        doc_id = f"DOC_{i+1:03d}" 
        source = ev.get("source", "未知来源")
        content = ev.get("content", "").strip()

        # 💡 数据清洗：去除异常空白符，并限制单篇长度（防止后续大模型超载）
        import re
        content = re.sub(r'\s+', ' ', content) 
        cleaned_content = content[:4000] if len(content) > 4000 else content

        # 组装成结构化字典
        structured_evidence.append({
            "doc_id": doc_id,
            "source": source,
            "content": cleaned_content
        })

    print(f"    ✅ 成功构建 {len(structured_evidence)} 条带编号的结构化证据！")
    
    # 将清洗好、贴好条形码的证据存入状态机，供 Synthesizer 使用
    return {"structured_evidence": structured_evidence}