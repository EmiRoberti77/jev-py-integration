from typesafe_sdk import Noul, TypeSafeClient, Choice
from config import get_key
api_key = get_key()
_base_url = 'https://ai-gateway.vercel.sh/typesafe'
print(api_key)
client = TypeSafeClient(
    api_key=api_key,
    base_url=_base_url
)
ticket = (
    "Hi, I've been trying to connect my Stripe account for 3 days "
    "and it keeps failing. I'm losing sales. Please help ASAP."
)

response = client.system_one(
    state=ticket,
    questions={
        'is_urgent': Noul(
            instructions='does this message express urgency'
        ),
        'team': Choice(
            instructions='which team should respond to the issue',
            criteria={
                'billing':'payment and subscription issue',
                'customer_service':'complaints and customer care',
                'tech_support':'tech team to support application faults'
            }
        )
    }
)

print(response.answers['is_urgent'].noul)
print(response.answers['team'].choice)