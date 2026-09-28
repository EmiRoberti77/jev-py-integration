from dotenv import load_dotenv
load_dotenv()

def get_key() -> str:
    import os
    api_key = os.getenv('TYPESAFE_API_KEY')
    if api_key is None:
        raise ValueError('Missing api key, set TYPESAFE_API_KEY in .env')
    return api_key