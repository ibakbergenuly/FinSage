import os
from mistralai import Mistral

def ask_mistral(question: str):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set")

    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return chat_response.choices[0].message.content
