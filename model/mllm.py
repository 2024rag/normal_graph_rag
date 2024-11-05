import requests
from PIL import Image
import io
import base64

def describe_image(img_obj, prompt):
    mllm_endpoint = "http://418891.proxy.nscc-gz.cn:8888"

    base64_encoded = _image_to_base64(img_obj)
    # Send base64_encoded to server
    url = f"{mllm_endpoint}/process_image"
    
    payload = {
        "image_base64": base64_encoded,
        "prompt": prompt
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        res = response.json()
        print(res)
        return res["data"]["response"]
    else:
        raise ValueError(f"infer error, error message:{response.json()}")

def _image_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_str