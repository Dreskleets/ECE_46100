import os
from huggingface_hub import InferenceClient, snapshot_download

def chat_with_model(selected_model):
    print("\nType 'exit' to end the conversation.")
    conversation = []
    while True:
        user_message = input("You: ")
        if user_message.strip().lower() == 'exit':
            return
        conversation.append({"role": "user", "content": user_message})
        completion = client.chat.completions.create(
            model=selected_model,
            messages=conversation
        )
        response = completion.choices[0].message.content
        print(f"AI: {response}\n")
        conversation.append({"role": "assistant", "content": response})

models = {
    "1": "deepseek-ai/DeepSeek-V3-0324",
    "2": "meta-llama/Meta-Llama-3-8B-Instruct",
    "3": "mistralai/Mistral-7B-Instruct-v0.2"
}

def select_model():
    print("Select an AI model to use:")
    for key, model in models.items():
        print(f"{key}: {model}")
    choice = input("Enter the number corresponding to your choice: ").strip()
    if choice not in models:
        print("Invalid choice. Exiting.")
        return None
    selected_model = models[choice]
    print(f"\nYou selected: {selected_model}")
    download_choice = input("Do you want to download this model locally? (y/n): ").strip().lower()
    if download_choice == 'y':
        print(f"Downloading model '{selected_model}'... This may take a while.")
        local_path = snapshot_download(repo_id=selected_model)
        print(f"Model downloaded to: {local_path}\n")
    return selected_model

def get_inference_client():
    return InferenceClient()

def chat_with_model(selected_model, client=None):
    if client is None:
        client = get_inference_client()
    print("\nType 'exit' to end the conversation.")
    conversation = []
    while True:
        user_message = input("You: ")
        if user_message.strip().lower() == 'exit':
            return
        conversation.append({"role": "user", "content": user_message})
        completion = client.chat.completions.create(
            model=selected_model,
            messages=conversation
        )
        response = completion.choices[0].message.content
        print(f"AI: {response}\n")
        conversation.append({"role": "assistant", "content": response})

def main():
    client = get_inference_client()
    selected_model = select_model()
    if not selected_model:
        return
    while True:
        chat_with_model(selected_model, client)
        again = input("Would you like to chat with another AI? (y/n): ").strip().lower()
        if again == 'y':
            selected_model = select_model()
            if not selected_model:
                break
        else:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()