md5_path="./data/md5.text"

#Chroma
collection_name="Chroma"
collection_path="./chroma"

#Splitters
chunk_size=1000
chunk_overlap=10
separators=["\n\n","\n",".",",","?","!","。","，"," ", "","？","！"]
min_check_split_num=1000  #允许分割的最小阈值

#Retriever
similarity_threshold=1

#Session
session_id = {
    "configurable": {
        "session_id": "user001"
    }
}

