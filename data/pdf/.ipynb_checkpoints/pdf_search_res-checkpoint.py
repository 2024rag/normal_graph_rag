from model.reranker.global_rerank import rerank
from tool import timer
from json_formatter import logger


class pdf_search_res:
    @timer
    def __init__(self, sentences_faiss, table_faiss, sentences_bm25, table_bm25, query, test):
        self.query = query
        self.test = test
        self.sentences_faiss = sentences_faiss
        self.sentences_bm25 = sentences_bm25

        logger.info(f"Query: {self.query}")

        if not test:
            self.table_faiss = table_faiss
            self.table_bm25 = table_bm25
            self.table = self.table_faiss
        else:
            self.table = []

        self.sentences = self.sentences_faiss
        for item in sentences_bm25:
            self.sentences.insert(0,item)

#         bm25_half = self.sentences_bm25[:len(self.sentences_bm25) // 2]

#         sentences_bm25_rerank = rerank([[self.query, item] for item in bm25_half])[0]
#         sentences_bm25_res = list(zip(bm25_half, sentences_bm25_rerank))

#         # Filter sentences with a rerank score greater than 3
#         sentences_bm25_res = [item for item in sentences_bm25_res if item[1] > 3]
        # for item in sentences_bm25_res:
        #     self.sentences.insert(0, item[0])
        #     print("Inserted item:", item)

    def get_raw(self):
        result = {
            "sentences_faiss": self.sentences_faiss,
            "sentences_bm25": self.sentences_bm25
        }
        if not self.test:
            result.update({
                "table_faiss": self.table_faiss,
                "table_bm25": self.table_bm25
            })
        return result

    def get(self, sentences_limit):
        if not self.test:
            if not self.sentences or len(self.sentences) <= 1:
                self.sentences = (
                    self.sentences_bm25[:8 if len(self.sentences_bm25) > 10 else len(self.sentences_bm25)]
                    + self.sentences_faiss[:8 if len(self.sentences_faiss) > 10 else len(self.sentences_faiss)]
                )

            if len(self.sentences) > sentences_limit:
                self.sentences = self.sentences[:sentences_limit]

            if self.table:
                self.table = [self.table[0]]

            return {
                "sentences": self.sentences,
                "table": self.table
            }
        else:
            return {
                "sentences": self.sentences
            }
