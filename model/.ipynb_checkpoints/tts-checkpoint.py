import os
import base64
from datetime import datetime
import uuid
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import requests
import base64

def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

key = "4839207162351487"  # AES-128 key
key = key.encode('utf-8')
data = "Gongsheng@2023"
encrypted_data = aes_encrypt(data, key)
encoded_data = base64.b64encode(encrypted_data)
output_dir="./output"

url = "http://193.163.19.81:9988/v1/gpt/tts"
headers = {
    "X-GS-User": "zhangyuxiang",
    "Content-Type": "application/json",
    "X-Symbiotic-Auth": encoded_data
}

def tts_convert(text, speech_id):
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_name = f"{speech_id}.mp3"
    output_path = os.path.join(output_dir, file_name)
    
    data = {
        "model": "tts-1",
        "voice": "nova",
        "text": text
    }
    response = requests.post(url, headers=headers, json=data)
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    return output_path