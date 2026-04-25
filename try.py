import os
from datetime import datetime
from dotenv import load_dotenv  # 导入读取.env的库
from langchain_openai import ChatOpenAI


load_dotenv()

# 从环境变量读取配置（不会泄露密钥）
api_key = os.getenv("MINIMAX_API_KEY")
base_url = os.getenv("MINIMAX_BASE_URL")
model_name = os.getenv("MINIMAX_MODEL_NAME")

# 初始化 Minimax (兼容 OpenAI 接口)
chat = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0
)

# 测试调用
if __name__ == "__main__":
    # res = chat.invoke("你好，请介绍一下自己")
    # print(res.content)
    res=datetime.now().strftime("%Y%m%d_%H%M%S")
    print(res,'\n',type(res))