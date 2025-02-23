import time
from utils.logger import logger
from tools.tools import tools_mapping
from tools.prompt import gen_prompt,user_prompt
from api.qwen2 import ModekProvider
""" 
to dos：
    1、 环境变量的设置
    2、 工具引入
    3、 prompt模板
    4、 模型初始化
    """
    
model_provider = ModekProvider()
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量
def parse_thoughts(response):
    """
        response:
        {
            "action":
            {
                "name":"action_name",
                "args":{
                    "arg_name":"arg_value",
                }
            },
            # agent的思考
            "thought":
            {
                "text":"agent的想法",
                "plan":"agent的工作规划",
                "criticism": "自我批判",
                "speak":"当前的步骤，返回给用户的总结信息",
                "reasoning":"agent的推理"
            }
        }
        """
    try:
        thoughts = response.get("thoughts")
        plan = thoughts.get('plan')
        observation = response.get('speak')
        reasoning = thoughts.get('reasoning')
        criticism = thoughts.get('criticism')
        prompt = f"""plan:{plan}\n
        observation:{observation}\n
        reasoning:{reasoning}\n
        criticism:{criticism}\n
        """
        return prompt
    except Exception as e:
        logger.error(f"agent_exacute error:{e}")
        return str(e)


def agent_excute(query,max_request_time = 30):
    cur_request_time = 0
    chat_history = []
    agent_scratch = '' # 用于模型反思等操作
    while cur_request_time < max_request_time:
        cur_request_time += 1
        # 如果返回结果达到预期结果，则直接返回
        """
        prompt包含的功能：
            1、 任务描述
            2、 工具描述
            3、 user_message
            4、 assistant_message
            5、 限制deep
            6、 给出更好的实现描述
        """
        sys_prompt = gen_prompt(query,agent_scratch)
        start_time = time.time()
        logger.info(f"{cur_request_time},开始调用llms")
        # call llms
        response = model_provider.chat(sys_prompt = sys_prompt,chat_history=chat_history)
        end_time = time.time()
        
        logger.info(f"{cur_request_time},结束调用llms,共耗时{end_time - start_time}")
        
        
        if not response or not isinstance(response,dict):
            logger.error(f"调用结果出错，结果如：{response},即将重试")
            continue
        
        """
        response:
        {
            "action":
            {
                "name":"action_name",
                "args":{
                    "arg_name":"arg_value",
                }
            },
            # agent的思考
            "thought":
            {
                "text":"agent的想法",
                "plan":"agent的工作规划",
                "criticism": "自我批判",
                "speak":"当前的步骤，返回给用户的总结信息",
                "reasoning":"agent的推理"
            }
        }
        """
        action_info = response.get('action')
        action_name = action_info.get('name')
        action_args = action_info.get('args')
        print(f"agent action: {action_name}")
        if action_name == "finish":
            final_answer = action_args.get('answer')
            logger.info(f"对于问题{query}的结果是：{final_answer}")
            break
        observation = response.get("thoughts").get("speak")
        try:
            # 执行action，action使用工具，工具通过action_name和funtion的匹配来调用
            func = tools_mapping.get(action_name)
            # 当前步骤的返回结果
            call_function_result  = func(**action_args)

            
        except Exception as e:
            logger.error(f"agent action call error: {e}")
            raise
        
        agent_scratch = agent_scratch + "\n: observation:{}\n execute action result: {}".format(observation,
                                                                                                call_function_result)
        user_message = user_prompt
        assistant_message = parse_thoughts(response)
        # result = f"这是{action_name}工具调用的结果:{observation}"
     
            
        chat_history.append([user_message,agent_scratch,assistant_message])
  
# agent 入口
def main():
    max_request_time = 30
    while True:
        query = input("请输入目标：")
        if query == "exit":
            return
        agent_excute(query,max_request_time = max_request_time)

if __name__ == '__main__':
   main()