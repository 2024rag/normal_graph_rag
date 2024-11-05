from sentence_transformers import SentenceTransformer


class bge_base_zh():
    def __init__(self):
        self.model=SentenceTransformer("/root/autodl-tmp/bge")

    def encode(self,sentences):
        return self.model.encode(sentences)



model=bge_base_zh()