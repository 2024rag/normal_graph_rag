
from unstructured.partition.pdf import partition_pdf
from config import pdf_loc
from model.llm.global_llm import llm
from tool import split_string_by_length, timer
from json_formatter import logger

@timer
def pdf_sum(pdf_name):
    elements=partition_pdf(pdf_loc(pdf_name))
    key_word=""
    for ele in elements:
        if ele.category=="Title":
            key_word+=ele.text+"\n"
    sum_part_array=[]
    logger.info(f"key_word: {key_word}")
    for index,item in enumerate(split_string_by_length(key_word,3500)):
        sum_part_array.append(f"第{index+1}部分:"+llm(f"""以下是文档的一个段落的关键词，请你根据这些关键词，去对文档的这个段落进行一次总结，简单来说，你要根据段落关键词去对该段落进行一次简要总结，并且输出总结即可。
文档的一个段落的关键词如下: {item}\n"""))

    sum_part="\n".join(sum_part_array)
    logger.info(f"sum_part: {sum_part}")

    return llm(f"""以下是一个文档的{len(sum_part_array)}个部分的总结，请你根据这几个部分的总结，去进行一次简要汇总，最后输出这个文档的总结。
文档的{len(sum_part_array)}个部分的总结:\n\n{sum_part}\n""")