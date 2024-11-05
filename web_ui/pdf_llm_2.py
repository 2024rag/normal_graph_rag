import os
import uuid
import base64
from typing import List, Dict
import streamlit as st
from PIL import Image
import io
from streamlit_chatbox import ChatBox, Markdown, Audio

from config import pdf_loc, zh
from controller.core import core
from controller.router import choose_task_path
from data.pdf.pdf_cls import pdf
from data.image.img_obj import image_obj
import json

from json_formatter import logger
from model.tts import tts_convert
from model.llm.global_llm import llm
from controller.image_chat import image_chat

def get_messages_history(history_len: int, content_in_expander: bool = False) -> List[Dict]:
    '''
    返回消息历史。
    content_in_expander控制是否返回expander元素中的内容，一般导出的时候可以选上，传入LLM的history不需要
    '''

    def filter(msg):
        content = [x for x in msg["elements"] if x._output_method in ["markdown", "text"]]
        if not content_in_expander:
            content = [x for x in content if not x._in_expander]
        content = [x.content for x in content]

        return {
            "role": msg["role"],
            "content": "\n\n".join(content),
        }

    return chat_box.filter_history(history_len=history_len, filter=filter)

chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)

def update_file_status():
    # 对之前处理的pdf列表与当前pdf列表 计算 差集
    # 当前pdf列表 st.session_state["file_upload"]
    # 之前的pdf列表 st.session_state['file_name']
    current_pdf_name = [pdf.name for pdf in st.session_state['file_upload']]
    print("status:", current_pdf_name, st.session_state['file_name'])
    pdf_to_del = list(filter(lambda pdf: pdf.pdf_name not in current_pdf_name, st.session_state['pdfs']))
    pdf_to_add = list(filter(lambda x: x.name not in st.session_state['file_name'], st.session_state['file_upload']))
    print("需要删除的pdf obj:", pdf_to_del)
    print("需要添加的pdf obj:", pdf_to_add)

    for del_pdf in pdf_to_del:
        # print(del_pdf.index)
        del st.session_state['pdfs'][del_pdf.index - 1]
    
    for add_pdf in pdf_to_add:
        with open(pdf_loc(add_pdf.name), "wb") as f:
            f.write(add_pdf.read())
        pdf_append=pdf(
            add_pdf.name,
            zh,
            test=False,
            load_mode=True
        )
        pdf_append.parse()

        st.session_state['pdfs'].append(pdf_append)
        st.session_state['file_name'].append(add_pdf.name)

    # 刷新pdf下标
    for index, pdf_item in enumerate(st.session_state['pdfs']):
        pdf_item.index=index+1
        st.session_state[index]=pdf_item     
        
def update_image_status():
    current_image_name = [image.file_id for image in st.session_state['image_upload']]
    image_to_del = list(filter(lambda image: image not in current_image_name, st.session_state['images'].keys()))
    image_to_add = list(filter(lambda image: image.file_id not in list(st.session_state['images'].keys()), st.session_state['image_upload']))
    print("需要删除的img obj:", image_to_del)
    print("需要添加的img obj:", image_to_add)

    for add_image in image_to_add:
        image_bytes = io.BytesIO(add_image.read())
        img_obj = Image.open(image_bytes)
        img = image_obj(
            img_name = add_image.file_id,
            img_obj = img_obj
        )
        img.describe()

        st.session_state['images'][add_image.file_id] = img

    for del_image in image_to_del:
        del st.session_state['images'][del_image]

def pdf_llm_2():

    # 自定义样式
    st.markdown(
        """
        <style>
        .audio-box {
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #30D5C8;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 上传情况: 
    # 1. 分区首次上传: 处理被更新了的分区 (图片 or 文件) 
    # 2. 分区更新:
    
    if "file_name" not in st.session_state: # processed pdf name
        st.session_state['file_name']=[]
    
    if "pdfs" not in st.session_state: # processed pdf obj
        st.session_state['pdfs']=[]

    if "images" not in st.session_state: # processed img obj
        st.session_state['images']={}
    
    if "speech" not in st.session_state:
        st.session_state['speech']=[]

    if "tasks" not in st.session_state:
        st.session_state['tasks']= 0

    if "history" not in st.session_state:
        st.session_state['history'] = []
    
    with st.sidebar:
        files = st.file_uploader(
            "上传知识文件：",
            [ ".pdf"],
            accept_multiple_files=True,
            on_change=update_file_status,
            key="file_upload"
        )
        image_files = st.file_uploader(
            "上传图片文件", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True,
            on_change=update_image_status,
            key="image_upload"
        )
       
        audio_status = st.toggle("输出文本音频")

    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter "
    chat_box.output_messages()
    if prompt := st.chat_input(chat_input_placeholder, key="kb_prompt"):
        logger.info(f"prompt: {prompt}")
        chat_box.user_say(prompt)

        task = choose_task_path(prompt, st.session_state['pdfs'], st.session_state['images'])
        print(f"任务类型：{task}")
        if task == 0:
            task_name = "日常对话"
            chat_box.ai_say([
                Markdown(f"执行{task_name}～", in_expander=False, title="回答"),
            ])
            res = llm(prompt)
            chat_box.update_msg(f"{res}", element_index=0, state="complete")
            
        elif task == 1:
            task_name = "文档问答"
            chat_box.ai_say([
                Markdown(f"执行{task_name}～", in_expander=False, title="回答结果"),
                Markdown(f"正在回答并搜索中 ...", in_expander=True, title="知识库匹配结果"),
            ])
            res=core(prompt, st.session_state['pdfs'])

            chat_box.update_msg(f"{res['response']}", element_index=0, state="complete")
            if 'search' in res:
                chat_box.update_msg(f"{res['search']}", element_index=1, state="complete")
            else:
                chat_box.update_msg(f"检测到非检索任务～", element_index=1, state="complete")
        
        elif task == 2:
            task_name = "图片问答"
            
            chat_box.ai_say([
                Markdown(f"执行{task_name}～", in_expander=False, title="回答结果"),
            ])

            res=image_chat(prompt, st.session_state['images'])
            chat_box.update_msg(f"{res}", element_index=0, state="complete")
        
        elif task == 3:
            task_name = ["文档问答", "图片问答"]
            
            chat_box.ai_say([
                Markdown(f"执行{task_name[0]}～", in_expander=False, title="回答结果"),
                 Markdown(f"执行{task_name[1]}～", in_expander=False, title="回答结果"),
                Markdown(f"正在回答并搜索中 ...", in_expander=True, title="知识库匹配结果"),
            ])

            img_res=image_chat(prompt, st.session_state['images'])
            pdf_res=core(prompt, st.session_state['pdfs'])
            chat_box.update_msg(f"{img_res}", element_index=0, state="complete")
            chat_box.update_msg(f"{pdf_res['response']}", element_index=1, state="complete")
            if 'search' in pdf_res:
                chat_box.update_msg(f"{pdf_res['search']}", element_index=2, state="complete")
            else:
                chat_box.update_msg(f"检测到非检索任务～", element_index=2, state="complete")
            

        if audio_status:
            speech_id = uuid.uuid4()
            st.session_state['speech'].append({speech_id: res['response']})
            speech_path = tts_convert(res['response'], speech_id)
            
        if audio_status:
            chat_box.ai_say(Audio(speech_path))