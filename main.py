import os

from config import zh
from controller.core import core
from data.pdf.pdf_cls import pdf
import streamlit as st
from streamlit_option_menu import option_menu
from web_ui.pdf_llm_2 import pdf_llm_2
from web_ui.gs_chat_web import gs_chat_web

if __name__=="__main__":


    st.set_page_config(
        "GS-Demo WebUI",
        os.path.join("img", "favicon.ico"),
        initial_sidebar_state="expanded",
        layout="wide",
        menu_items={
            'About': f"""欢迎体验XX demo！"""
        }
    )

    pages={
            "文件问答": {
                "icon": "file",
                "func": pdf_llm_2,
            },
        
            "对话":{
                "icon":"chat",
                "func":gs_chat_web
            }
    }

    with st.sidebar:
        # st.image(
        #     os.path.join(
        #         "img",
        #         "logo白.svg"
        #     ),
        #     use_column_width=True
        # )
        options=list(pages)
        icons=[x["icon"] for x in pages.values()]

        default_index=0
        selected_page=option_menu("",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,)
    if selected_page=="文件问答":
        pages[selected_page]["func"]()
    if selected_page=="GS对话":
        pages[selected_page]['func']()

    






