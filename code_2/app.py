from config import get_jev_config, get_jev_key, get_llm_key
from anthropic import Anthropic
from typesafe_sdk import Choice, Noul, TypeSafeClient
from messages import TEST_TICKETS

QUESTIONS = {
    'is_urgent': Noul(instructions='Is the mesasage time sensitive'),
    'is_angry': Noul(instructions='does the client seem angry or frustrated'),
    'needs_a_human': Noul(instructions='Does this message require a human decision or input, is the message legal, large refund over £200, a threat of any kind'),
    'intent': Choice(
        instructions='what is the client main request',
        criteria={
            'refund':'the customer wants money returned',
            'technical_help':'the customer needs a bug or a technical fix',
            'spam':'the content is not relevant or marketing related',
            'other':'none of the criteria fits'
        }
    )
}

def handle(message:str, jev:TypeSafeClient, llm:Anthropic):
    r = jev.system_one(model=get_jev_config().model, state={'ticket':message}, questions=QUESTIONS)
    urgent = r.nouls['is_urgent'].noul
    angry = r.nouls['is_angry'].noul
    human = r.nouls['needs_a_human'].noul
    intent = r.choices['intent'].choice
    print(message)
    print('============')
    print(f'{urgent=}', f'{angry=}', f'{human}')
    print(f'{intent=}')

def main():
    jev = TypeSafeClient(api_key=get_jev_key(), base_url=get_jev_config().base_url)
    llm = Anthropic(api_key=get_llm_key())
    for msg in TEST_TICKETS:
        handle(msg, jev, llm)
    return 0

if __name__ == '__main__':
    main()