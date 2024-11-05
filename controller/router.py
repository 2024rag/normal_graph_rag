from model.llm.gs_bgchat import gs_bgchat


def choose_task_path(prompt, pdf_obj, img_obj):
    """

    RETURN:
        0: 纯大模型对话
        1: 文档问答
        2: 图片问答
        3: 1,2都要回答
    """
    if len(pdf_obj) == 0 and len(img_obj) == 0:
        return 0
    
    elif len(pdf_obj) != 0 and len(img_obj) == 0:
        return 1

    elif len(pdf_obj) == 0 and len(img_obj) != 0:
        return 2

    elif len(pdf_obj) != 0 and len(img_obj) != 0:
        task_id = judge_topic(prompt)
        return task_id

    return 0

def judge_topic(prompt):
    judge_prompt = """
请你根据用户输入的指令，判断该指令可能属于哪一类任务：(日常对话类，文档问答类，图片问答类)

以下是部分输入输出样例：
例子1:
输入：红楼梦是谁写的？
输出：日常对话类
例子2:
输入：图片中有什么东西呢？
输出：图片问答类
例子3:
输入：文档中的xx是什么？
输出：文档问答类

现在请你根据用户指令进行判断：
输入："""
    topic_prompt = judge_prompt + prompt + '\n' + "输出："
    topic = gs_bgchat(topic_prompt)

    print(topic)
    if "日常对话" in topic:
        return 0
    if "文档问答" in topic:
        return 1
    if "图片问答" in topic:
        return 2

    return 0
