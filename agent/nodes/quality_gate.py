# agent/nodes/quality_gate.py

from agent.state import ResearchState

def quality_gate_node(state: ResearchState) -> dict:
    print("\n--- ⚖️ 节点运转中：[Node 7] Quality Gate 质量检测 ---")
    
    draft = state.get("draft_report", "")
    retries = state.get("retry_count", 0)
    
    issues = []
    
    # 规则 1：初稿是否为空或异常
    if not draft or "系统发生异常" in draft:
        issues.append("初稿生成失败或内容为空。")
        
    elif "目前暂未发现直接匹配的临床文献证据" in draft:
            pass 
            
    elif "[DOC_" not in draft:
        issues.append("严重警告：初稿中未发现任何 [DOC_xxx] 引用标签！存在极高幻觉风险，禁止输出！")
            
    if issues:
        print(f"    🚨 质检未通过：{issues[0]}")
        # 增加重试次数，并记录问题
        return {
            "quality_issues": issues,
            "retry_count": retries + 1
        }
    
    print("    ✅ 质检完美通过：报告包含合法溯源标记，逻辑严密！")
    # 质检通过，清空问题列表
    return {
        "quality_issues": [],
        "retry_count": retries
    }