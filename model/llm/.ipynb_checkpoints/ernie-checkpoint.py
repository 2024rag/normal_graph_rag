import json

import requests

from model.baidu_get_access_token import baidu_get_access_token
from tool import cont_str_len


def ernie(chat):
    chat = cont_str_len(chat, 7900)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + baidu_get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": chat
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    return response.json()['result']