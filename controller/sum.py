from typing import List

from data.pdf.pdf_cls import pdf
from model.llm.global_llm import llm


def sum_(query,pdf_array:List[pdf]):
    pdf_sum_array=[f"第{item.index}个文档的总结: {item.sum}\n\n" for item in pdf_array]
    return llm(f"""现在你要根据现有的文档总结，去回答用户的问题。
    用户的问题: {query}
    
    现有的文档总结:
    
    {"".join(pdf_sum_array)}
""")


