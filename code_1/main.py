from config import get_key
from typesafe_sdk import Choice, Noul, TypeSafeClient

_base_url = 'https://api.typesafe.ai'
_model = 'jev-latest'


def main():
    api_key = get_key()

    with TypeSafeClient(
        api_key=api_key,
        base_url=_base_url
    ) as client:
        response = client.system_one(
            model=_model,
            state={
                "ticket":"I was charged twice and need a duplicate refunded today."
            },
            questions={
                "is_urgent": Noul(instructions="Does the ticket explicitly communicate time pressure?"),
                "intent": Choice(
                instructions="What is the customer's main request?",
                criteria={
                        "refund": "The customer wants money returned.",
                        "technical_help": "The customer needs a bug or integration fixed.",
                        "other": "None of the other options clearly fits.",
                    },
                ),
            }
        )
        print(response)
        print('Urgent probability:', response.nouls['is_urgent'].noul)


if __name__ == "__main__":
    main()
