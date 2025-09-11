import os
from huggingface_hub import InferenceClient, snapshot_download

# List of available models
models = {
    "1": "deepseek-ai/DeepSeek-V3-0324",
    "2": "meta-llama/Meta-Llama-3-8B-Instruct",
    "3": "mistralai/Mistral-7B-Instruct-v0.2"
}

# Display model options
print("Select an AI model to use:")
for key, model in models.items():
    print(f"{key}: {model}")

# Get user input
choice = input("Enter the number corresponding to your choice: ").strip()

# Validate choice
if choice not in models:
    print("Invalid choice. Exiting.")
    exit(1)

selected_model = models[choice]
print(f"\nYou selected: {selected_model}")

# Ask if user wants to download the model
download_choice = input("Do you want to download this model locally? (y/n): ").strip().lower()

if download_choice == 'y':
    print(f"Downloading model '{selected_model}'... This may take a while.")
    local_path = snapshot_download(repo_id=selected_model)
    print(f"Model downloaded to: {local_path}\n")

# Create inference client
client = InferenceClient()

# Create a chat completion
completion = client.chat.completions.create(
    model=selected_model,
    messages=[
        {
            "role": "user",
            "content": "How many 'G's in 'huggingface'?"
        }
    ],
)

# Display response
print("\nResponse from the model:")
print(completion.choices[0].message.content)
