import time
import streamlit as st
from knowledge_base import KnowledgeBaseService


# 基于streamlit第三方库构造前端。

# streamlit的特性：在每次网页刷新和网页内容发生变化后，都会重新运行整个脚本，这会导致变量的反复初始化。
# 因此，在使用stremlit构建前端时，需要利用st.session_state(dict)维护变量。


st.title("知识库更新服务")

upload_file=st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False
)

if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()

if upload_file is not None:
    #收集文件基础信息
    file_name=upload_file.name
    file_type=upload_file.type
    file_size=upload_file.size / 1024 # 转换成KB

    st.subheader(f"文件名:{file_name}")
    st.write(f"文件类型:{file_type} | 文件大小:{file_size:.2f} KB")

    text=upload_file.getvalue().decode("utf-8")

    with st.spinner("数据加载中..."):
        time.sleep(1)
        show_res=st.session_state["service"].upload_file_chroma(text,file_name)
        st.write(show_res)