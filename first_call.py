from typesafe_sdk import Noul, TypeSafeClient
from config import get_key
api_key = get_key()
print(api_key)
client = TypeSafeClient(
    api_key=api_key
)
ticket = (
    "Hi, I've been trying to connect my Stripe account for 3 days "
    "and it keeps failing. I'm losing sales. Please help ASAP."
)

response = client.system_one(
    state=ticket,
    questions={
        'urgency': Noul(
            instructions='does this message express urgency'
        )
    }
)

print(response.answers['urgency'].noul)