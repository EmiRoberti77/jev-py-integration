from dotenv import load_dotenv
load_dotenv()

def get_key() -> str:
    import os
    api_key = os.getenv('AI_GATEWAY_API_KEY')
    if api_key is None:
        raise ValueError('Missing api key')
    return api_key