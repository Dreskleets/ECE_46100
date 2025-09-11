import os
from huggingface_hub import InferenceClient

client = InferenceClient()
while True:
    user_model = input("Enter the model name (e.g., deepseek-ai/DeepSeek-V3-0324):\n")

    print(f"*****Type 'exit' or 'quit' to end the chat*****\n\n.")
    while True:
        content = input("What would you like to ask?\n")
        if content.lower() in ['exit', 'quit']:
                print("Exiting the program.")
                break
        completion = client.chat.completions.create(
            model= user_model,
            messages=[
            {
                "role": "user",
                "content": content
            }
     ],
        )

        print(completion.choices[0].message)