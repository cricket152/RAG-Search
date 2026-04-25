学习视频：

[RAG项目-01、RAG项目案例介绍_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1yjz5BLEoY?spm_id_from=333.788.videopod.episodes&vd_source=e199874f35cfaf2a2bb9aac6ed6a25a8&p=46)

在参考视频复刻代码的基础上，我又添加了删除历史记录和新建对话的功能，可有可无的功能，不讲不讲。

# 一.离线文件上传功能
---
- app_file-upload.py：“前端”，基于Streamlit构建
- knowledge_base.py：存储组件。使用md5编码查重的方式来检测该文件是否已经被存储进知识库内。内置KnowledgeBaseService类，内置了向量化和分割语段的组件

```python
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
```

这里存储进向量库需要数据和对应的“元数据”，这里使用的是创建一份元数据映射在多份不同数据内容的策略。

```python
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
```

# 二.RAG检索功能
---
## 检索器

vector_stores.py用于专门构建检索器
```python
def get_retriever(self):
	retriever=self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})
	return retriever
```

## 对话链

rag.py用于构造chain

# 三.历史记录功能
---
在file_memory.py中添加好我们实现复写好的负责长期记忆功能的类对象，写好接口。

```python
def get_history_chat(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")
```

在rag.py中导入它，这里要尤其注意接口的适配，可以通过打印的方式一点点debug掉。

```python
#接收内容：“{'input': '我体重180斤，尺码推荐', 'history': []}”，需要规范接口
def format_retriever_input(text):
    return text["input"]

#接收内容：{'input': {'input': '我体重180斤，尺码推荐', 'history': []}, 'context': '身高：155-165cm， 体重：75-95 斤，建议尺码S。\n身高：160-170cm， 体重：90-115斤，建议尺码Mn身高：170-178cm
# ， 体重：130-150斤，建议尺码XL。\n身高：175-182cm， 体重：145-165斤，建议尺码2XL。\n身高：178-185cm， 体重：160-180斤，建议尺码3XL。\n身高：180-190建议尺码5XL。\n'}
#需要规范接口
def format_dict_input(text:dict):
    new_dict={}
    new_dict["input"]=text["input"]["input"]
    new_dict["history"]=text["input"]["history"]
    new_dict["context"]=text["context"]
    return new_dict
```

功能写好后创建app_chat.py构造前端，尤其注意Streamlit架构每次内容改变都会刷新，所以需要把想要留存的东西都存在st.session_state里面（如对话记录，创建对话链）

# 四.闲聊
---
AI发展的实在是太快了，未来不会写点什么AI相关的项目实在说不过去，于是花了几天时间恶补了一下langchain的相关知识。

这个项目带给我的主要有以下几点：

1. Debug的能力：都报错，回溯找到报错的源头，中途打印找报错原因与修复方法。
2. 创建config.py管理配置：把需要经常调整的配置信息放在一个文件里，既方便管理，又能使整个项目架构变清晰。

无话可说了。继续加油喵~

