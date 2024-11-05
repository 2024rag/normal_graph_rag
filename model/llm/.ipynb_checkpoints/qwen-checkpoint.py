from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask,request
app = Flask(__name__)

device = "cuda"  # 指定使用CUDA作为计算设
model = AutoModelForCausalLM.from_pretrained(
    "/root/autodl-tmp/qwen2.5",  # 模型路径
    torch_dtype="auto",  # 数据类型自动选择
    device_map="auto",
    load_in_4bit=True
)

tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/qwen2.5")


@app.route("/chat",methods=["POST"])
def chat():
    data=request.get_json()
    messages=data.get("messages")
#     messages = [
#     {"role": "system", "content": "你是一个智能AI助手"},  # 系统角色消息
#     {"role": "user", "content": prompt}  # 用户角色消息
# ]
# 使用分词器的apply_chat_template方法来格式化消息
    text = tokenizer.apply_chat_template(
    messages,  # 要格式化的消息
    tokenize=False,  # 不进行分词
    add_generation_prompt=True  # 添加生成提示
)

    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    
    generated_ids = model.generate(
    model_inputs.input_ids,  # 模型输入的input_ids
    max_new_tokens=512  # 最大新生成的token数量
)

# 从生成的ID中提取新生成的ID部分
    generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)
    return response
def qwen(prompt):
    messages=[
        {"role":"user","content":prompt}
    ]
#     messages = [
#     {"role": "system", "content": "你是一个智能AI助手"},  # 系统角色消息
#     {"role": "user", "content": prompt}  # 用户角色消息
# ]
# 使用分词器的apply_chat_template方法来格式化消息
    text = tokenizer.apply_chat_template(
    messages,  # 要格式化的消息
    tokenize=False,  # 不进行分词
    add_generation_prompt=True  # 添加生成提示
)

    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    
    generated_ids = model.generate(
    model_inputs.input_ids,  # 模型输入的input_ids
    max_new_tokens=512  # 最大新生成的token数量
)

# 从生成的ID中提取新生成的ID部分
    generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)
    return response

if __name__=="__main__":
    app.run(debug=True)

