import json
from typing import List

import requests


def gs_reranker(pairs):
    url="http://385513.proxy.nscc-gz.cn:8888/rerank_infer"
    data=json.dumps({
        "pairs":pairs
    })
    headers={
        "Content-Type":"application/json"
    }
    response=requests.request("POST",url,headers=headers,data=data)
    if type(response.json()['data']['scores']) is not List:
        return [response.json()['data']['scores']]
    else:
        return response.json()['data']['scores']