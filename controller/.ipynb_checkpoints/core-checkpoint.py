import os
from typing import List

from retry import retry

from controller.mention import mention, IS_MENTION
from controller.sum import sum_
from controller.talk import talk
from data.pdf.pdf_cls import pdf
from model.llm.global_llm import llm, TYPE_TASK
from json_formatter import logger
import json

def core(query,pdf_array:List[pdf]):

    for item in pdf_array:
        stem,_=os.path.splitext(item.pdf_name)
        query=query.replace(item.pdf_name,f"第{item.index}个文档").replace(stem,f"第{item.index}个文档")
    SUM = "1"
    SEARCH = "2"
    def classify(query):
        classify_id= llm(f"""你是一分类机器人，你要根据输入，进行分类。
                你的输出可以是两种，1.当你认为输入是想汇总或者总结报告时，输出 {SUM}
                                  2.当你认为输入是想搜索关键信息时，输出 {SEARCH}
                                
                注意:你只可以输出这两种，不需要输出其他东西。
                例子:
                1.输入:"告诉我这个报告的大致内容"
                  输出:{SUM}
                2.输入:"告诉我，员工啥时候上下班"
                  输出:{SEARCH}
                3.输入:"告诉我这个报告的大致内容，并且告诉我员工上下班的时间"
                  输出:{SUM}
                4.输入:"给我讲讲123报告中的断电存储波形"
                  输出:{SEARCH}
                5.输入:"告诉我r141e中的主要内容是什么"
                  输出:{SUM}
                6.输入:"怎么打开车窗"
                  输出:{SEARCH}

                输入:"{query}"
                输出:
    """,type=TYPE_TASK)
        return SEARCH
        if classify_id!=SUM  and classify_id!=SEARCH:
            return SEARCH
        else:
            return classify_id
            
    def classify_exec(classify_id,pdf_array,query):
        if classify_id==SEARCH:
            response,search=talk(query, pdf_array)
            return {
                "response":response,
                "search":search
                }
        elif classify_id==SUM:
            return {
                "response":sum_(query,pdf_array)
            }

    classify_id=classify(query)
    logger.info(f"classify_id: {classify_id}")

    mention_res,mention_flag=mention(query,pdf_array)

    logger.info(f"mention_res: {mention_res}  mention_flag: {mention_flag}")

    if mention_flag==IS_MENTION:
        return classify_exec(classify_id,[item for item in pdf_array if item.index in mention_res ] , query)
    else:
        return classify_exec(classify_id,pdf_array,query)