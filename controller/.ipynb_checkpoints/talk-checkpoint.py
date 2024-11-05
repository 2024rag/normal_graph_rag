from typing import List
from data.pdf.pdf_cls import pdf
from model.llm.global_llm import llm
from model.llm.global_llm import llm
from json_formatter import logger
import streamlit as st

def format_history_entry(role: str, content: str) -> dict:
    return {"role": role, "content": content}

def update_history(query: str):
    if len(st.session_state['history']) == 2:
        st.session_state['history'][0] = format_history_entry("user", st.session_state['last_prompt'])

    if len(st.session_state['history']) >= 4:
        st.session_state['history'] = [format_history_entry("user", st.session_state['last_prompt'])] + st.session_state['history'][3:]

def get_pdf_content(pdf_obj: pdf, query: str, top_k: int) -> tuple:
    pdf_search = pdf_obj.search(query, top_k).get(15)
    sentences = "\n".join(set(pdf_search["sentences"]))
    table = "\n".join(set(pdf_search["table"])) if not pdf_obj.test else ""
    return sentences, table

def handle_single_pdf(query: str, pdf_obj: pdf) -> str:
    sentences, table = get_pdf_content(pdf_obj, query, top_k=50)
    logger.info(f"table: {table}")
    
    user_prompt = f"""现在，你要根据现有的文档内容与文档表格去回答用户的问题。
用户的问题是: {query}
请你根据以下文档内容与文档表格去回答用户的问题
{f"你现有的文档表格:{table}" if table else ""}
你现有的文档内容:{sentences}
你的回答:"""
    
    st.session_state['history'].append(format_history_entry("user", user_prompt))
    # talk_res = gs_history_chat(st.session_state['history'])
    talk_res=llm(user_prompt)
    st.session_state['history'].append(format_history_entry("assistant", talk_res))
    st.session_state['last_prompt'] = query
    
    return talk_res, sentences

def handle_multiple_pdfs(query: str, pdf_array: List[pdf]) -> str:
    top_k = 50
    pdf_search_array = [
        {"index": item.index, "sentences": "\n".join(set(item.search(query, top_k).get(int(30/len(pdf_array)))["sentences"])),
         "table": "\n".join(set(item.search(query, top_k).get(int(30/len(pdf_array)))["table"]))}
        for item in pdf_array
    ]
    
    sentences = "\n\n".join([f"第{item['index']}个文档的文档内容: {item['sentences']}" for item in pdf_search_array])
    table = "\n\n".join([f"第{item['index']}个文档的文档表格: {item['table']}" for item in pdf_search_array if item['table']])
    logger.info(f"table: {table}")
    
    user_prompt = f"""现在你要根据现有的文档内容与文档表格去回答用户的问题。
用户的问题是: {query}
请你根据以下文档内容与文档表格去回答用户的问题
{table}
{sentences}
你的回答:"""
    
    st.session_state['history'].append(format_history_entry("user", user_prompt))
    res = gs_history_chat(st.session_state['history'])
    st.session_state['history'].append(format_history_entry("assistant", res))
    st.session_state['last_prompt'] = query
    
    return res, sentences

def talk(query: str, pdf_array: List[pdf]) -> tuple:
    update_history(query)
    
    if len(pdf_array) == 1:
        return handle_single_pdf(query, pdf_array[0])
    
    if len(pdf_array) > 1:
        return handle_multiple_pdfs(query, pdf_array)