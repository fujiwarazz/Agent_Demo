from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量
# 使用pydantic_settings库实现配置管理

class Settings(BaseSettings):
    """应用配置类"""
    
    # 服务配置
    HOST: str = os.getenv("HOST", "0.0.0.0")  # 服务监听地址
    PORT: int = int(os.getenv("PORT", "8804"))  # 服务端口
    WORKERS: int = int(os.getenv("WORKERS", "4"))  # 工作进程数
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY")
    model_name: str = os.getenv("MODEL_NAME","qwen-plus")
    max_retry_times: int = int(os.getenv("MAX_RETRY_TIMES", "3"))
    workdir_root: str = os.getenv("WORKDIR_ROOT","./data/llm_result")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY")

    
    # 日志配置
    LOG_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")  # 日志目录
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # 日志级别
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"  # 日志格式
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"  # 日期格式
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", str(10 * 1024 * 1024)))  # 单个日志文件最大大小
    
    class Config:
        env_file = ".env"

settings = Settings() 