import time
import streamlit as st
import config_data as config
from datetime import datetime
from rag import RegService
from file_memory import get_history_chat

"""
对话主界面，基于StreamLit架构实现
"""

st.title("智能客服服务")
st.divider()

prompt=st.chat_input()

#保存历史对话
if "message" not in st.session_state:
    st.session_state["message"]=[{"role":"assistant","input":"你好！有什么能帮到你的吗？"}]

#创建对话实例对象
if "rag" not in st.session_state:
    st.session_state["rag"]=RegService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["input"])

with st.sidebar:
    st.title("操作")

    #清楚对话历史功能
    if st.button("清除对话历史"):
        history=get_history_chat(config.session_id["configurable"]["session_id"])
        history.clear()
        st.session_state["message"] = [{"role":"assistant","input":"对话历史已清除，请问还有什么需要帮助的？"}]
        #显示成功
        st.success("清除成功！")
        st.rerun()

    #新建对话功能
    if st.button("新建对话"):
        config.session_id["configurable"]["session_id"]=datetime.now().strftime('%Y%m%d_%H%M%S')
        #重置前端
        st.session_state["message"] = [{"role":"assistant","input":"新对话已创建，请问有什么需要帮助的？"}]
        st.rerun()

#对话功能
dialog_memory=[]

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","input":prompt})

    with st.spinner("思考中..."):

        #由于我们要采用流式输出，“迭代器”中的内容需要专门开设一个函数用于抓包，利用yield原封返回
        def capture(generator,memory):
            for chunk in generator:
                memory.append(chunk)
                yield chunk

        time.sleep(1)
        res=st.session_state["rag"].chain.stream({"input":prompt},config.session_id)
        st.chat_message("assistant").write_stream(capture(res,dialog_memory))
        st.session_state["message"].append({"role":"assistant","input":"".join(dialog_memory)})