from model.llm.Yi import Yi
from model.llm.ernie import ernie
from model.llm.gs_bgchat import gs_bgchat,gs_chat_stream
from tokenizer.tokenizer import tokenizer
from model.llm.qwen import qwen

TYPE_CHAT="1"
TYPE_TASK="0"
def llm(chat,type=TYPE_CHAT, stream=False):
    llm_ret=qwen(chat)
#   if len(tokenizer.encode(chat)) >8000:
#     chat=tokenizer.decode(tokenizer.encode(chat)[:8000])
#     print(chat)
    
#   if type==TYPE_CHAT:
#     llm_ret = gs_bgchat(chat, stream)
#     return llm_ret
#   if type==TYPE_TASK:
#     llm_ret=gs_bgchat(chat, stream)
    return llm_ret

def stream_llm(chat, stream=True):
  yield gs_chat_stream(chat, stream)