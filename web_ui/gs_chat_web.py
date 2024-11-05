from streamlit_chatbox import ChatBox, Markdown
import streamlit as st
from model.llm.global_llm import llm, stream_llm
from model.llm.gs_bgchat import gs_bgchat,gs_chat_stream
import os

from typing import List,Dict
chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)

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

def gs_chat_web():
    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter "
    history = get_messages_history(0)
    chat_box.output_messages()
    if prompt := st.chat_input(chat_input_placeholder, key="kb_prompt"):
        chat_box.user_say(prompt)
        chat_box.ai_say("")
        text = ""
        res = gs_chat_stream(prompt, stream=True)
        # print(res)
        for token_res in res:
            try:
                token_choice = token_res.get('choices','')[0]
                finish_reason = token_choice.get('finish_reason')
                if finish_reason == 'stop':
                    break
                text += token_res['choices'][0]['delta']['content']
                # print(text)
            except Exception as e:
                print(e)
        
            chat_box.update_msg(text)
        print(text)
        chat_box.update_msg(text)