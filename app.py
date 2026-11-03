
import requests

url = "http://localhost:11434/api/generate"

print("================================")
print("       SMARTCHAT AI")
print("================================")
print("Type 'exit' to close the chatbot.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("SmartChat: Goodbye!")
        break

    data = {
        "model": "llama3.2:1b",
        "prompt": question,
        "stream": False
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        print("\nSmartChat:", result["response"])
        print()

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)
