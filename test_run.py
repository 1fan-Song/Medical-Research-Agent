import os
from dotenv import load_dotenv
from agent.graph import build_graph
import time

load_dotenv()


def main():
    print("🏥 医疗科研 Agent 系统初始化中...\n")
    
    # 构建并编译图
    app = build_graph()

    # 定义我们要提问的初始病历/科研问题
    initial_state = {
        "research_question": "TP53基因突变对非小细胞肺癌（NSCLC）患者使用PD-1抑制剂的疗效有什么影响？"
    }

    print("================ 开始流转 ================\n")
    
    # 正式启动智能体工作流！
    final_state = app.invoke(initial_state)

    print("\n================ 流转结束 ================\n")

    # ==========================================
    # 最终结果的安全打印 (防止缺斤少两报错)
    # ==========================================
    print("🎯 [最终检验] Planner 扩充的检索词:")
    for q in final_state.get("search_queries", []):
        print(f"  - {q}")

    print("\n📚 [最终检验] Retriever 提取的真实证据:")
    for ev in final_state.get("evidence", []):
        print(f"  - [{ev.get('source', '未知网址')}]\n    摘要: {ev.get('content', '无内容')[:100]}...") # 摘要太长只打印前100字

    print("\n" + "="*50)
    print("📝 [最终检验] Synthesizer 生成的医学综述报告:")
    print("="*50)
    print(final_state.get("final_report", "未生成报告"))
    print("="*50 + "\n")

    # ... 原有的打印代码 ...
    report_content = final_state.get("final_report", "未生成报告")
    
    # 保存为本地文件
    file_name = f"Research_Report_{int(time.time())}.md"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n✅ 专业的医学综述报告已保存至: {file_name}")

# 这是整个文件的绝对最末尾，点火开关！
if __name__ == "__main__":
    main()