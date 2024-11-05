import json
from typing import List


from data.pdf.pdf_cls import pdf
from model.llm.global_llm import llm, TYPE_TASK

IS_MENTION="1"
NOT_MENTION="0"
def mention(query,pdf_array:List[pdf]):
    mention_flag=llm(f"""现在，你要判断用户是否提到了或者想使用某个文档。
    若提到了要使用某个特定文档，则输出: {IS_MENTION}
    若没有提到具体要用哪个文档，则输出: {NOT_MENTION}
    
    用户说的话: {query}
    
    你的输出:
""",type=TYPE_TASK)
    print(mention_flag)
    if mention_flag==IS_MENTION:
        mention_res_json_mode=["文档的排序号","文档的排序号"]
        try:
             mention_res=json.loads(llm(f"""现在，你要根据用户说的话，去提取用户想要使用的文档的排序号，并且以json格式，格式化输出，输出格式为:{json.dumps(mention_res_json_mode)}
                      文档的排序号的意思是文档的顺序编号，例如，第1个文档，则这个文档的排序号是1，第2个文档，则这个文档的排序号是2。
                      注意:若不是第2个文档，而是第二个文档，则该文档的排序号也是2，其他也同理，例如第三个文档，第四个文档等。
                      例子:用户说的话: 第1个文档和第2个文档之间的主要区别是什么？
                          你的输出: [1,2]

                      现在，用户说的话是: {query}
                      你的输出:
              """,type=TYPE_TASK).replace("```","").replace("json",""))
        except:
            return None,NOT_MENTION
        
         
        print(mention_res)
        res=[item for item in mention_res if item in [pdf_item.index for pdf_item in pdf_array]]
        if res==[]:
            return None,NOT_MENTION
        return res,IS_MENTION
    else:
        return None,NOT_MENTION