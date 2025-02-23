import os
import ollama
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import json

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant. and your response should be able to be load in json'},
        {'role': 'user', 'content': '你是谁？'}],
    )
    
print(json.loads(completion.choices[0].message.content))