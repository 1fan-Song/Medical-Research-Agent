# agent/nodes/citation_resolver.py

import re
from agent.state import ResearchState

def citation_resolver_node(state: ResearchState) -> dict:
    print("\n--- 🔗 节点运转中：[Node 6] Citation Resolver 渲染学术引用 ---")
    
    draft = state.get("draft_report", "")
    evidence_list = state.get("structured_evidence", [])
    
    # 1. 提取所有单一的 DOC_xxx 编号 (不带括号，方便统计去重)
    all_doc_ids = re.findall(r'DOC_\d{3}', draft)
    
    unique_doc_ids = []
    for doc in all_doc_ids:
        if doc not in unique_doc_ids:
            unique_doc_ids.append(doc)
            
    if not unique_doc_ids:
        print("    ⚠️ 初稿中未发现引用标签。")
        return {"citations_mapping": {}, "references_list": ""}
        
    # 2. 构建映射表和参考文献列表
    citations_mapping = {}
    references_lines = ["\n---\n### 📚 参考文献 (References)\n"]
    
    for i, doc_id in enumerate(unique_doc_ids, 1):
        citations_mapping[doc_id] = str(i) # 比如把 "DOC_001" 映射为 "1"
        
        # 查找来源
        source_info = "未知来源"
        for ev in evidence_list:
            if ev["doc_id"] == doc_id:
                source_info = ev["source"]
                break
                
        references_lines.append(f"[{i}] {source_info}")
        
    # 3. 高级替换逻辑：处理合并引用 [DOC_001, DOC_002] -> [1, 2]
    resolved_draft = draft
    # 找到所有被 [] 包裹的内容，里面可能包含多个 DOC_xxx
    brackets_content = re.findall(r'\[(.*?)\]', resolved_draft)
    
    for content in brackets_content:
        # 如果这个括号里包含 DOC_ 字符，说明是引用标签
        if "DOC_" in content:
            new_content = content
            # 把里面的 DOC_xxx 替换成对应的数字
            for doc_id, num in citations_mapping.items():
                new_content = new_content.replace(doc_id, num)
            # 把整个括号里的内容替换掉
            resolved_draft = resolved_draft.replace(f"[{content}]", f"[{new_content}]")
            
    references_list = "\n".join(references_lines)
    
    print(f"    ✅ 成功渲染了 {len(citations_mapping)} 条学术引用！")
    
    return {
        "draft_report": resolved_draft, 
        "citations_mapping": citations_mapping,
        "references_list": references_list
    }