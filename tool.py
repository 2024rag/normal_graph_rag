import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import requests
import base64
import os
import uuid
from datetime import datetime
from json_formatter import logger

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

url = "http://193.163.19.81:9988/v1/gpt/tts"
headers = {
    "X-GS-User": "zhangyuxiang",
    "Content-Type": "application/json",
    "X-Symbiotic-Auth": encoded_data
}

# 创建 output 文件夹(如果不存在)
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def cont_str_len(str,cont_len):
    if len(str)>=cont_len:
        while True:
            print("xiujian")
            str=str[:int(len(str)*0.8)]
            if len(str)<cont_len:
                return str
    return str


def split_string_by_length(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]


def timer(func):
    def func_in(*args, **kwargs):
        start_time = time.time()
        func_res = func(*args, **kwargs)
        end_time = time.time()
        spend_time = (end_time - start_time)
        print(f"Function '{func.__name__}' took {spend_time:.6f} seconds to execute.")
        logger.info(f"Function '{func.__name__}' took {spend_time:.6f} seconds to execute.")
        return func_res
    return func_in


def reciprocal_rank_fusion(rankings, k=60):
    """
    Reciprocal Rank Fusion (RRF) implementation in Python.

    Parameters:
    - rankings: A list of lists, where each inner list represents the rankings from a different system.
      Each element in the inner lists should be a document identifier.
    - k: A constant used in the RRF formula, typically set to 60.

    Returns:
    - A dictionary with document identifiers as keys and their fused RRF scores as values.
    """
    # Initialize a dictionary to store the RRF scores for each document
    rrf_scores = {}

    # Iterate over each ranking list
    for rank in rankings:
        for i, doc in enumerate(rank):
            # Calculate the reciprocal rank for the current document
            reciprocal_rank = 1.0 / (k + i + 1)  # Adding 1 because index starts at 0

            # If the document is already in the rrf_scores dictionary, update its score
            if doc in rrf_scores:
                rrf_scores[doc] += reciprocal_rank
            else:
                # Otherwise, add the document to the dictionary with its reciprocal rank as the initial score
                rrf_scores[doc] = reciprocal_rank

    # Return the RRF scores, sorted by score in descending order
    return dict(sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True))




def tts_convert(text):
    """将文本转换为语音并保存到文件中."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_name = f"{timestamp}_{unique_id}.mp3"
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