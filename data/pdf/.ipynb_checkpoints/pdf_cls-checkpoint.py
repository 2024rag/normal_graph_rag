from config import zh, dim, pdf_loc
from data.faiss.faiss_controller import faiss_controller
from data.pdf.bm25_chinese import bm25_chinese
from data.pdf.get_pdf_table import get_pdf_table
from data.pdf.pdf_search_res import pdf_search_res
from data.pdf.pdf_sum import pdf_sum
from data.pdf.spliter import split_chinese, split_english
from model.embed.global_embed import embedding
from model.llm.global_llm import llm
from .pdf_utils import get_pdf_raw_blocks
from tool import timer
import os
import json

import fitz
from json_formatter import logger


class pdf:
    def __init__(self,pdf_name,language,index=-1,test=False,load_mode=False):

        self.index=index
        self.test=test
        self.pdf_name=pdf_name
        self.language=language
        self.test=test
        self.load_mode=load_mode

        self.save_path=f'./Persistence/{self.pdf_name.split(".")[0]}'

    @timer
    def parse(self):
        self.faiss_sentences=faiss_controller(dim)
        self.faiss_table=faiss_controller(dim)

        if self.load_mode==True and os.path.exists(self.save_path):
            self.load()
            return

        if self.test==False:
            self.parse_doc_summary()
            self.parse_docs_table()

        self.split_docs()
        embed_sentences = self.get_sentence_embeddings()
        self.faiss_sentences.vector_add(embed_sentences)

        self.save()

    def save(self):
        os.makedirs(self.save_path)

        self.faiss_sentences.index_save(self.save_path+"/sentences.index")
        self.faiss_table.index_save(self.save_path+"/table.index")

        with open(self.save_path+"/sum.txt","w") as f:
            f.write(self.sum)
        with open(self.save_path+"/sentences.json",'w') as f:
            json.dump(self.sentences,f, ensure_ascii=False, indent=4)
        with open(self.save_path+"/table.json",'w') as f:
            json.dump(self.table,f, ensure_ascii=False, indent=4)
        
        logger.info("save done!")
        print("save done!")

    def load(self):
        print(f"{self.pdf_name} is exist!")

        with open(self.save_path+"/sentences.json",'r') as f:
            self.sentences=json.load(f)
        with open(self.save_path+"/table.json",'r') as f:
            self.table=json.load(f)
        with open(self.save_path+"/sum.txt","r") as f:
            self.sum=f.read()
            
        self.faiss_sentences.index_load(self.save_path+"/sentences.index")
        self.faiss_table.index_load(self.save_path+"/table.index")
        
        logger.info("load done !")
        print("load done !")
    
    @timer
    def search(self,query,top_k):
        sentences_index=self.faiss_sentences.vector_search(embedding([query]),top_k,110)

        sentences_faiss = [self.sentences[index] for index in sentences_index]

        sentences_bm25 = ["".join(bm25_sorted_item[1]) for bm25_sorted_item in
                          sorted(bm25_chinese(self.sentences, query), reverse=True)]

        if self.test==False:
            table_index = self.faiss_table.vector_search(embedding([query]), top_k,150)

            if self.table==[]:
                table_faiss=[]
                table_bm25=[]
            else:
                table_faiss = [self.table[index] for index in table_index]

                table_bm25 = ["".join(bm25_sorted_item[1]) for bm25_sorted_item in
                              sorted(bm25_chinese(self.table, query), reverse=True)]

            return pdf_search_res(sentences_faiss, table_faiss, sentences_bm25, table_bm25,query,self.test)

        if self.test==True:

            return pdf_search_res(sentences_faiss,None,sentences_bm25,None,query,self.test)

    @timer
    def split_docs(self):

        if self.language==zh:
            self.sentences = split_chinese("".join(get_pdf_raw_blocks(self.pdf_name)))
            logger.info(f"{self.sentences}")
        else:
            self.sentences = split_english()
    
    @timer
    def get_sentence_embeddings(self):
        embed_sentences=embedding(self.sentences)
        print("len_embed_sentences:",len(embed_sentences))
        logger.info(f"len_embed_sentences: {len(embed_sentences)}")
        return embed_sentences
    
    def parse_docs_table(self):
        self.table = get_pdf_table(self.pdf_name) # TODO 最耗时，后续可以优化
        # self.table = []

        self.faiss_table = faiss_controller(dim)
        self.faiss_table.vector_add(embedding(self.table))
        logger.info(f"table: {self.table}")
    
    def parse_doc_summary(self):
        # self.sum=pdf_sum(self.pdf_name) # 总结pdf
        self.sum = ""