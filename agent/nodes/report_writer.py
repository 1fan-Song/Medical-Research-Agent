# agent/nodes/report_writer.py

from datetime import datetime
from agent.state import ResearchState

def report_writer_node(state: ResearchState) -> dict:
    print("\n--- 📇 节点运转中：[Node 8] Report Writer 排版导出 ---")
    
    # 拿到渲染好的正文 和 参考文献列表
    draft = state.get("draft_report", "未生成初稿")
    refs = state.get("references_list", "")
    
    # 获取真实的当前系统时间 (解决之前 2023 年的问题)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 构建精美的 Markdown 文件头
    header = f"> **报告生成时间**: {current_time}\n> **系统驱动**: Multi-Agent Medical Research System\n\n---\n\n"
    
    # 拼装最终的报告
    final_report = header + draft + "\n" + refs
    
    print("    ✅ 最终精美排版完成！准备写入文件...")
    return {"final_report": final_report}