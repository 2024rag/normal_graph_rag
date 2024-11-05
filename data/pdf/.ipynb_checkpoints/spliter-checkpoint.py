import re

def split_chinese(raw_text):
    pattern=r'[。]'
    split_text=re.split(pattern,raw_text)
    return [text for text in split_text if text]

def split_english(raw_text):
    # 匹配句号、问号和感叹号作为句子的分隔符
    pattern = r'[.!?]'
    split_text = re.split(pattern, raw_text)
    return [text.strip() for text in split_text if text.strip()]