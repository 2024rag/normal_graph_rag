from ..data.pdf.pdf_cls import pdf
from model.llm.gs_bgchat import gs_history_chat

class PDFInterface():
    def __init__(self) -> None:
        self.raw_chat_prompt="请根据用户提供文档内容，结合文档与用户提问进行回答。\n\n文档：\n{file}\n\n用户提问：{query}\n请回答："
        self.pdf = ""
        
    def pdf_raw_chat(self, messages, pdf_files):
        content = self._get_pdf_content(pdf_files)
        chat_prompt = self.raw_chat_prompt.format(file=content, query=messages[-1]['content'])
        # TODO gs chat
        pdf_message = [{"role":"user", "content":chat_prompt}]
        res = gs_history_chat(pdf_message)
        return res

    def pdf_search_chat(self, messages, pdf_files):
        ...
    
    def _get_pdf_content(self):
        # TODO get pdf_content
        ...