import http
import json

import numpy as np
import requests


def gs_embed(text):
    url="http://127.0.0.1:35989/emb_infer"
    data=json.dumps({
        "text":text,
        "type":"base"
    })
    headers={
        "Content-Type":"application/json"
    }
    response=requests.request("POST",url,headers=headers,data=data)
    
    return np.array(response.json()['data']['embeddings'])