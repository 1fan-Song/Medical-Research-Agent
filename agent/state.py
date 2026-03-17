from typing import TypedDict, List, Annotated,Dict
import operator
from langchain_core.messages import BaseMessage

# ---------------------------------------------------------
# 1. 结构化定义：单条证据 (完美复刻你文档里的底层逻辑)
# ---------------------------------------------------------
class Evidence(TypedDict):
    source_type: str    # 数据来源，例如 "pubmed_abstract" 或 "pdf" [cite: 65]
    doc_id: str         # 文献编号，例如 PMID 或内部 PDF id [cite: 66]
    snippet: str        # 证据原文片段（控制长度，防幻觉的绝对核心） [cite: 72]
    claim_support: str  # 这条证据支持的“子问题/结论点”标签 [cite: 73]

# ---------------------------------------------------------
# 2. 全局流转单：ResearchState (贯穿整个 LangGraph)
# ---------------------------------------------------------
class ResearchState(TypedDict):
    # 1. 基础输入与规划
    research_question: str
    search_queries: List[str]
    
    # 2. 原始检索层 (重点：使用 Annotated 和 operator.add 支持并行写入)
    raw_evidence: Annotated[List[Dict], operator.add] 
    
    # 3. 证据构建层
    structured_evidence: List[Dict] 
    
    # 4. 生成与引用层
    draft_report: str           # 包含 [PMID:xxx] 这种原始标签的初稿
    citations_mapping: Dict     # 引用映射表，如 {"PMID:xxx": "[1]", "Local_PDF:xxx": "[2]"}
    references_list: str        # 最终拼接好的参考文献列表文本
    
    # 5. 质量控制层
    quality_issues: List[str]   # 如果质检不合格，裁判会把修改意见写在这里
    retry_count: int            # 记录重试次数，防止无限死循环
    
    # 6. 最终输出
    final_report: str           # 经过渲染和排版后的终稿