from sentence_transformers import SentenceTransformer


class bge_base_zh():
    def __init__(self):
        self.model=SentenceTransformer("D:\\pyproject\\tod\\model\\embed\\BAAI-bge-base-zh-v1.5")

    def encode(self,sentences):
        return self.model.encode(sentences)



model=bge_base_zh()