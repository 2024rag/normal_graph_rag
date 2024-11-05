
from model.llm.gs_bgchat import gs_bgchat

def image_chat(prompt, image_obj):
    image_prompt = ""
    
    for value in image_obj.values():
        image_prompt += value.img_description
        image_prompt+= "\n\n"
    
    bg_prompt = "以上是关于一些图片的文字描述，如果之后的提问与图片相关则结合以上图片描述信息进行回答。如果不相关，则针对用户问题进行回答。\n\n 用户问题："

    prompt = image_prompt + bg_prompt + prompt + "\n"

    res = gs_bgchat(prompt)
    return res
    