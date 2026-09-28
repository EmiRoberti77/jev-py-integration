from config import get_jev_config, get_jev_key, get_llm_key, LLM_TYPE
from anthropic import Anthropic
from openai import OpenAI
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

def handle_reply(llm:OpenAI | Anthropic, message:str, tone:str='apologetic'):
    msg = f'Write a {tone} reply to:\n\n{message}'
    
    if isinstance(llm, Anthropic):
        r = llm.messages.create(
            model='claude-sonnet-5',
            max_tokens=400,
            messages=[{'role':'user', 'content':msg}]
        )
        return r.content[0].text

    if isinstance(llm, OpenAI):
        r = llm.responses.create(
            model='gpt-4.1-mini',
            max_output_tokens=400,
            input=msg
        )
        return r.output_text

    raise TypeError('ERR: Unsupported LLM Type')

def handle(message:str, jev:TypeSafeClient, llm:OpenAI | Anthropic) -> dict:
    r = jev.system_one(model=get_jev_config().model, state={'ticket':message}, questions=QUESTIONS)
    urgent = r.nouls['is_urgent'].noul
    angry = r.nouls['is_angry'].noul
    human = r.nouls['needs_a_human'].noul
    intent = r.choices['intent'].choice
    print(message)
    print('============')
    print(f'{urgent=}', f'{angry=}', f'{human=}')
    print(f'{intent=}')
    if intent == 'spam':
        return {'action':'drop'}

    if urgent > 0.8 or angry > 0.8 or human > 0.7:
        return {'action': 'reply', 'reply': handle_reply(llm=llm, message=message)}

    return {'action': 'normal'}

def main() -> None:
    jev = TypeSafeClient(api_key=get_jev_key(), base_url=get_jev_config().base_url)
    llm = OpenAI(api_key=get_llm_key(LLM_TYPE.OPENAI))
    for msg in TEST_TICKETS:
        action = handle(msg, jev, llm)
        if action.get('action') == 'reply':
            print('llm reply', action['reply'])
    

if __name__ == '__main__':
    main()