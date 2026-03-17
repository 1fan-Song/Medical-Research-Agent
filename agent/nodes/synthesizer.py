# agent/nodes/synthesizer.py

import os
import requests
from agent.state import ResearchState
from datetime import datetime
# 🛡️ 绝对保留你的神级提示词，一字不改！
SYNTHESIZER_PROMPT = """你是一位顶尖的肿瘤科主治医师。
请根据提供的【检索到的证据】撰写医学报告。

【进阶撰写要求】
1. 即使没有绝对肯定的结论，也请总结目前的【研究趋势】。
   - 比如：虽然临床疗效数据不一，但证据 [PMID: XXX] 提示 TP53 突变可能通过重塑免疫微环境来影响免疫逃逸。
2. 区分【机制研究】与【临床疗效】：如果证据里提到了对免疫微环境的影响，请务必写出来。
3. 搜索关键词：如果证据中提到了 PD-L1 表达、TMB（肿瘤突变负荷）与 TP53 的关系，请作为间接证据引用。
4. 依然保持严谨：不要捏造数据，但要尽力从现有文字中提取有价值的科研线索。"""

# ... 顶部的 SYNTHESIZER_PROMPT 保持不变 ...

def synthesizer_node(state: ResearchState) -> dict:
    print("\n--- ✍️ 节点运转中：[Node 5] Synthesizer 生成初稿 ---")

    current_date = datetime.now().strftime("%Y年%m月%d日")  

    question = state["research_question"]
    evidence_list = state.get("structured_evidence", [])
    
    if not evidence_list:
            print("    ⚠️ 证据库为空，直接输出无证据声明，跳过大模型深度推理。")
            draft_report = "针对您提出的问题，经过对 PubMed 及本地知识库的全面检索，**目前暂未发现直接匹配的临床文献证据**。\n\n这通常意味着该研究方向（如：针对特定耐药机制的新型联合疗法）属于极度前沿的探索区，相关的大规模临床试验数据尚未公开发表。建议持续关注即将召开的国际肿瘤学大会（如 ASCO, ESMO）的最新摘要发布。"
            return {"draft_report": draft_report}
    else:
        evidence_text = "\n".join([f"[{e.get('doc_id')}] 来源: {e.get('source', '未知')}\n摘要内容: {e.get('content', '')}" for e in evidence_list])
    
    user_content = f"【原始问题】\n{question}\n\n【检索到的带编号证据】\n{evidence_text}\n\n【附加引用要求】\n请务必在陈述事实时，在对应句子的末尾使用上述证据的编号进行引用（例如：[DOC_001]）。"

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_API_BASE", "").strip()
    model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

    if base_url.endswith("/chat/completions"):
        endpoint = base_url
    else:
        if base_url.endswith("/"): base_url = base_url[:-1]
        if not base_url.endswith("/v1"): base_url += "/v1"
        endpoint = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYNTHESIZER_PROMPT},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.5 
    }

    print("    🧠 主治医师正在阅读带编号的证据，撰写医学初稿...")
    
    # 💡 引入重试装甲！
    max_retries = 3
    draft_report = ""
    
    for attempt in range(max_retries):
        try:
            print(f"      📡 正在请求大模型 (第 {attempt + 1}/{max_retries} 次尝试，允许思考 150 秒)...")
            # 把 timeout 放宽到 150 秒
            response = requests.post(endpoint, headers=headers, json=payload, timeout=150)
            response.raise_for_status()
            
            resp_data = response.json()
            draft_report = resp_data["choices"][0]["message"]["content"]
            print("    ✅ 初稿生成完毕！")
            break # 成功则跳出循环
            
        except Exception as e:
            print(f"    ❌ 第 {attempt + 1} 次生成初稿失败: {e}")
            if attempt < max_retries - 1:
                print("      ⏳ 休息 3 秒后重试...")
                import time
                time.sleep(3)
            else:
                draft_report = f"系统发生异常，重试 3 次后仍无法生成完整报告。原始证据如下：\n{evidence_text}"

    return {"draft_report": draft_report}