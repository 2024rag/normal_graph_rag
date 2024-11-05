import jieba
from gensim.summarization import bm25
from tool import timer

@timer
def bm25_chinese(sentences,word):
    corpus=[]
    for sentence in sentences:
        corpus.append(list(jieba.cut(sentence)))
    bm25Model=bm25.BM25(corpus)
    scores=bm25Model.get_scores(list(jieba.cut(word)))
    return zip(scores,corpus)