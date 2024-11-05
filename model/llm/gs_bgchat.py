import requests
from tokenizer.tokenizer import tokenizer

def gs_history_chat(messages):
    if len(messages)==1:
        if len(tokenizer.encode(messages[0]['content'])) >8000:
            chat=tokenizer.decode(tokenizer.encode(messages[0]['content'])[:8000])
            # print(chat)
            messages[0]['content']=chat
    elif len(messages)==3:
        all_text="\n".join([item['content'] for item in messages])
        if len(tokenizer.encode(all_text)) >8000:
            pre_token_len=len(tokenizer.encode("\n".join([item['content'] for item in messages][:-1])))
            print("pre_token_len:",pre_token_len)
            chat=tokenizer.decode(tokenizer.encode(messages[-1]['content'])[:8000-pre_token_len])
            messages[-1]={
                "role":"user",
                "content":chat
            }
    
    url = "http://385366.proxy.nscc-gz.cn:8888/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    print("end_messages: ",messages)
    data = {
        "model": "gs-llm",
        "messages": messages,
        "max_tokens": 8192,
        "temperature": 0
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.text)
    if response.status_code == 200:
        res = response.json()
        res = res["choices"][0]
        return res["message"]['content'].replace("�","")
    else:
        raise ValueError("infer error")
    

LLM_URL = "http://385366.proxy.nscc-gz.cn:8888/v1/chat/completions"
def gs_bgchat(prompt, stream=False):
    print(len(prompt))
    url = LLM_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gs-llm",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 8192,
        "temperature": 0.3,
        "stream": stream
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.text)
    if response.status_code == 200:
        res = response.json()
        res = res["choices"][0]
        return res["message"]['content'].replace("�","")
    else:
        raise ValueError("infer error")


def gs_chat_stream(prompt, stream=True):
    url = LLM_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gs-llm",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 8192,
        "temperature": 0.3,
        "stream": stream
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        event_data = decoded_line.replace('data: ', '').strip()
                        print(event_data)
                        if '["finish_reason": "stop"]' in event_data:
                            print("Received end signal. Stopping listener.")
                            break  # 结束循环

                        # 尝试将 JSON 字符串解析为字典
                        data_dict = json.loads(event_data)
                        yield data_dict

        except Exception as e:
            print(e)
            response.close()
        finally:
            # 断开连接
            response.close()
    else:
        raise ValueError("infer error")