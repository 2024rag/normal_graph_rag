import faiss
from tool import timer


class faiss_controller:
    def __init__(self,dimension):
        # self.index=faiss.IndexHNSWFlat(dimension,32)
        self.index=faiss.IndexFlat(dimension)

    def vector_add(self,vector):
        self.index.add(vector)

    def index_save(self,location):
        faiss.write_index(self.index,location)

    def index_load(self,location):
        self.index=faiss.read_index(location)


    @timer
    def vector_search(self,vector,top_k,limit):
        distance,index=self.index.search(x=vector,k=top_k)
        filter_distance=[index for index,item in enumerate(distance[0]) if item<limit ]
        filter_index=[index[0][distance_index] for distance_index in filter_distance ]
        return filter_index