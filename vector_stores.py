from re import search
from langchain_chroma import Chroma
import config_data as config

'''
用于构造chain链中的retriever检索项
'''

class VectorStoreService:
    def __init__(self,embedding):
        self.vector_store=Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding,
            persist_directory=config.collection_path
        )

    def get_retriever(self):
        retriever=self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})
        return retriever
    
if __name__=="__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    vector_store_service=VectorStoreService(DashScopeEmbeddings())
    retriever=vector_store_service.get_retriever()

    print(retriever.invoke("我体重180斤，尺码推荐"))