# agent/nodes/retriever.py

import time
from Bio import Entrez
from agent.state import ResearchState

def retriever_node(state: ResearchState) -> dict:
    print("\n--- 🔍 节点运转中：[Retriever] 真实 PubMed 官方检索 (BioPython) ---")
    queries = state.get("search_queries", [])
    
    if not queries:
        queries = [state.get("research_question", "")]
        
    print(f"📡 准备调用 Bio.Entrez 向 PubMed 发送请求...")
    
    # ⚠️ 极其重要：NCBI 规定必须留下邮箱，否则会封杀 IP
    # 这里用一个虚拟邮箱，或者你可以换成你自己的南科大/深理工邮箱
    Entrez.email = "syf_research@example.com"
    
    all_evidence = []
    
    for i, q in enumerate(queries[:2]):
        print(f"  [{i+1}/2] 正在检索 PubMed: {q[:40]}...")
        try:
            # 1. 搜索文献 ID
            handle = Entrez.esearch(db="pubmed", term=q, retmax=10) 
            record = Entrez.read(handle)
            handle.close()

            id_list = record.get("IdList", [])
            
            if not id_list:
                print("    ⚠️ 未找到匹配的文献。")
                continue
                
            print(f"    🔗 找到文献 IDs: {id_list}，正在拉取摘要文本...")
            
            # 2. 拉取摘要正文 (Abstract)
            fetch_handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="text")
            abstracts_text = fetch_handle.read()
            fetch_handle.close()
            
            print(f"\n    📄 【PubMed 摘要预览】:\n    {abstracts_text[:200]}...\n")
            
            all_evidence.append({
                "source": f"PubMed IDs: {','.join(id_list)}",
                "content": abstracts_text[:20000] # 给大模型提供充足的文本
            })
            
            time.sleep(1) # NCBI 要求的礼貌延迟
            
        except Exception as e:
            print(f"  ❌ 检索发生网络错误: {e}")
            continue
            
    print(f"✅ 成功从 PubMed 抓取到 {len(all_evidence)} 组真实的文献摘要！")
    return {"raw_evidence": all_evidence}