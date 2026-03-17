# agent/graph.py

from langgraph.graph import StateGraph, START, END

from agent.state import ResearchState
from agent.nodes.planner import planner_node
from agent.nodes.retriever import retriever_node as pubmed_searcher_node
from agent.nodes.evidence_builder import evidence_builder_node
from agent.nodes.synthesizer import synthesizer_node
from agent.nodes.citation_resolver import citation_resolver_node
from agent.nodes.report_writer import report_writer_node

# 👇 导入最后拼上的两块真实拼图
from agent.nodes.pdf_retriever import pdf_retriever_node
from agent.nodes.quality_gate import quality_gate_node

def check_quality(state: ResearchState):
    issues = state.get("quality_issues", [])
    retries = state.get("retry_count", 0)
    
    if issues and retries < 2:
        print("    🔄 触发重试机制，打回重做...")
        # 如果质检不合格，打回合成器重新写！
        return "rebuild_report"
    else:
        return "generate_report"

def build_graph():
    workflow = StateGraph(ResearchState)

    # 1. 注册 8 大护法 (全部换成了真实函数)
    workflow.add_node("planner", planner_node)
    workflow.add_node("pubmed_searcher", pubmed_searcher_node)
    workflow.add_node("pdf_retriever", pdf_retriever_node)
    workflow.add_node("evidence_builder", evidence_builder_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("citation_resolver", citation_resolver_node)
    workflow.add_node("quality_gate", quality_gate_node)
    workflow.add_node("report_writer", report_writer_node)

    # 2. 编排工作流
    workflow.add_edge(START, "planner")
    
    # 并发双路检索
    workflow.add_edge("planner", "pubmed_searcher")
    workflow.add_edge("planner", "pdf_retriever")
    
    # 汇流至构建器
    workflow.add_edge("pubmed_searcher", "evidence_builder")
    workflow.add_edge("pdf_retriever", "evidence_builder")
    
    # 线性流转
    workflow.add_edge("evidence_builder", "synthesizer")
    workflow.add_edge("synthesizer", "citation_resolver")
    workflow.add_edge("citation_resolver", "quality_gate")
    
    # 质量控制路由
    workflow.add_conditional_edges(
        "quality_gate", check_quality,
        {
            "rebuild_report": "synthesizer", # 打回 Node 5 重写
            "generate_report": "report_writer" # 放行 Node 8
        }
    )
    workflow.add_edge("report_writer", END)

    return workflow.compile()