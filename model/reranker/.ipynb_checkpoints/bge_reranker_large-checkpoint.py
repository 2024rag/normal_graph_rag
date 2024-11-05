import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification


class bge_reranker_large():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('/ignore/bge_reranker_large')
        self.model = AutoModelForSequenceClassification.from_pretrained('/ignore/bge_reranker_large')

    def get_scores(self,pairs):
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores=self.model(**inputs,return_dict=True).logits.view(-1,).float()
            return scores.tolist()


model=bge_reranker_large()