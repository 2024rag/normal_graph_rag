from tool import timer
from model.reranker.gs_reranker import gs_reranker
@timer
def rerank(pairs):
    return gs_reranker(pairs)