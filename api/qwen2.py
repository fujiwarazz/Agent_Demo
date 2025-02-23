import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from tools.prompt import user_prompt
import json
from config.config import settings
from utils.logger import logger


# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=os.getenv("DASHSCOPE_API_KEY"), 
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': '我要让你作为AI猫娘'},
#         {'role': 'assistant', 'content': '好的'},
#         {'role': 'user', 'content': '你是谁'},
#         ],
#     )
    
# print(completion.choices[0].message.content)
class ModekProvider(object):
    def __init__(self):
        self.api_key = settings.dashscope_api_key 
        self.model_name = settings.model_name
        self._client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.max_retry_times = settings.max_retry_times
        
    def chat(self,sys_prompt,chat_history=[]):
        cur_retry_times = 0
        while cur_retry_times < self.max_retry_times:
            cur_retry_times +=1
            try:
                messages = [{'role': 'system', 'content': sys_prompt}]
                for message in chat_history:
                    messages.append({'role': 'user', 'content': message[0]})
                    messages.append({'role': 'assistant', 'content': message[1]})
                messages.append({'role': 'user', 'content': user_prompt})
                completion = self._client.chat.completions.create(
                                model=self.model_name,
                                messages= messages)
                print(f'completion:{completion.choices[0].message.content}')
                if completion.choices[0].message.content.startswith("```json"):
                    print(f'修改后completion:{completion.choices[0].message.content[7:-3]}')
                    
                    return json.loads(completion.choices[0].message.content[7:-3])
                return json.loads(completion.choices[0].message.content)
            except Exception as e:
                logger.error(f"调用模型失败，completion：{completion.choices[0].message.content}")
                print(f"{cur_retry_times},调用模型失败，原因：{e}")
                
            return {}