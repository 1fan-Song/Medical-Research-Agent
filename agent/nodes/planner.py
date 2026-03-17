# agent/nodes/planner.py
import os
import json
import requests
import time
from agent.state import ResearchState

PLANNER_PROMPT = """你是一位顶尖的生物信息学与临床医学专家。
请将用户输入的医学科研问题，拆解并扩充为 2 到 3 个高度专业的 PubMed 英文检索式（包含同义词和 MeSH 词）。

【严格输出要求】
必须输出合法的 JSON 数据，绝不要带 Markdown 标记，格式如下：
{
    "queries": ["检索式1", "检索式2"]
}"""

def planner_node(state: ResearchState) -> dict:
    print("\n--- 🧠 节点运转中：[Planner] 拆解并扩展医学问题 ---")
    question = state["research_question"]
    print(f"收到原问题: {question}")

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_API_BASE", "").strip()
    model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

    if not api_key or not base_url:
        print("❌ 致命错误：缺失 OPENAI_API_KEY 或 OPENAI_API_BASE 环境变量！")
        return {"search_queries": [question]}

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
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.1
    }

    max_retries = 3
    queries = [] 
    
    for attempt in range(max_retries):
        try:
            print(f"📡 正在向大模型发送请求 (第 {attempt + 1}/{max_retries} 次尝试)...")
            response = requests.post(endpoint, headers=headers, json=payload, timeout=120)
            response.raise_for_status() 
            
            resp_data = response.json()
            raw_content = resp_data["choices"][0]["message"]["content"].strip()

            # 👇 这里是完整清理 Markdown 的逻辑
            if raw_content.startswith("```json"): 
                raw_content = raw_content[7:]
            elif raw_content.startswith("```"): 
                raw_content = raw_content[3:]
            if raw_content.endswith("```"): 
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()

            parsed_json = json.loads(raw_content)
            queries = parsed_json.get("queries", [])

            if not queries:
                raise ValueError("JSON 解析成功，但 queries 列表为空")

            print(f"✅ 成功生成专业检索式: {queries}")
            break 

        except Exception as e:
            print(f"❌ Planner 节点请求或解析失败: {e}")
            if 'response' in locals():
                print(f"服务器真实返回: {response.text}")
            
            if attempt < max_retries - 1:
                print("⏳ 休息 2 秒后准备重试...\n")
                time.sleep(2)

    if not queries:
        print("⚠️ 启用兜底策略：直接使用原问题作为检索词。")
        queries = [question]

    return {"search_queries": queries}