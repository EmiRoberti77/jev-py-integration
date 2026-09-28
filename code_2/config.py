from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()
_base_url = 'https://api.typesafe.ai'
_model = 'jev-latest'
class JevConfig(BaseModel):
    base_url:str = Field(description='base url for jev', default=_base_url)
    model:str = Field(description='jev model',default=_model)

def get_jev_key() -> str:
    import os
    api_key = os.getenv('TYPESAFE_API_KEY')
    if api_key is None:
        raise ValueError('JEV Missing api key, set TYPESAFE_API_KEY in .env')
    return api_key

def get_llm_key() -> str:
    import os
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key is None:
        raise ValueError('ANTHROPIC_API_KEY Missing api key')
    return api_key

def get_jev_config():
    return JevConfig()
