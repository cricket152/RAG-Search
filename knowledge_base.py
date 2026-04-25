import os
import hashlib
import config_data as config
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

'''
知识库管理模块：
利用md5编码查重，将不同的资料文档保存在知识库中。
'''


#检查文件内是否有相同的md5值
def check_md5(md5_str:str):

    """
    检查传入的md5_str是否已经存在于md5.text文件中。
    如果存在，返回True；如果不存在，返回False。
    """

    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding="utf-8").close()  # 如果文件不存在，创建一个空文件
        return False
    else:
        for line in open(config.md5_path,'r',encoding="utf-8").readlines():
            line=line.strip()
            if line==md5_str:
                return True
        return False

#将md5值保存在文件中
def save_md5(md5_str:str):
    with open(config.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_str+'\n')

#获取文本md5值
def get_md5_string(text:str,encoding="utf-8"):
    md5_str=hashlib.md5(text.encode(encoding)).hexdigest()
    return md5_str

class KnowledgeBaseService:

    def __init__(self):
        #如果路径不存在先创建
        os.makedirs(config.collection_path,exist_ok=True)

        #初始化Chroma
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config.collection_path,
        )

        #初始化分割器
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators
        )

    #数据存储进向量库
    def upload_file_chroma(self,data:str,filename:str):
        md5_data=get_md5_string(data)

        #查重
        if check_md5(md5_data):
            return "[跳过]该文件已存储进向量库"

        #判断是否符合分割条件
        if len(data)>config.min_check_split_num:
            splitted_data=self.spliter.split_text(data)
        else:
            splitted_data=[data]

        metadata={
            "file":filename,
            "operator":"Cricket",
            "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #存储进向量库
        self.chroma.add_texts(
            texts=splitted_data,
            metadatas=[metadata for _ in splitted_data],
        )

        save_md5(md5_data)
        
        return "[成功]数据存储成功！"


if __name__=="__main__":
    service=KnowledgeBaseService()
    print(service.upload_file_chroma("窗边的蟋蟀","test.txt"))