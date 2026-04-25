import os
import config_data as config
from dotenv import load_dotenv
from langchain_core.documents import Document
from vector_stores import VectorStoreService
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from file_memory import get_history_chat
'''
用于构造对话链chain
'''

load_dotenv()
api_key = os.getenv("MINIMAX_API_KEY")
base_url = os.getenv("MINIMAX_BASE_URL")
model_name = os.getenv("MINIMAX_MODEL_NAME")

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

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

class RegService:
    def __init__(self):
        self.retriever=VectorStoreService(DashScopeEmbeddings()).get_retriever()
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system","请根据提供的参考资料和用户问题，给出符合参考资料内容、准确的答案，"
                    "参考资料：{context}"
                    "这是你和用户的历史对话信息："
                ),
                MessagesPlaceholder("history"),  #注意这里的“占位”需要放在元组外
                (
                    "human","这是用户提出的问题，请回答：{input}"
                )
            ]
        )
        self.model=ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model_name
        )

        self.chain=self.__get_chain()

    def format_doc(self,docs:list[Document]):
        context=""
        
        for doc in docs:
            context+=doc.page_content+"\n"

        return context

    #构造链
    def __get_chain(self):
        chain=(
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_retriever_input) | self.retriever | self.format_doc
            } | RunnableLambda(format_dict_input) | self.prompt_template | print_prompt | self.model | StrOutputParser()
        )

        #加入历史对话信息
        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history_chat,
            input_messages_key="input",
            history_messages_key="history"
        )

        return conversation_chain

if __name__=="__main__":
    session_id={
        "configurable":{
            "session_id":"user001"
        }
    }
    reg_service=RegService()
    query="我体重180斤，尺码推荐"

    result=reg_service.chain.invoke({"input":query},session_id)
    print(result)