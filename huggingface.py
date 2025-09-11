import os
import time
import sqlite3
from huggingface_hub import InferenceClient, snapshot_download

def chat_with_model(selected_model):
    total_time = 0.0
    times_chatted = 0
    print("\nType 'exit' to end the conversation.")
    conversation = []
    while True:
        user_message = input("You: ")
        if user_message.strip().lower() == 'exit':
            break
        conversation.append({"role": "user", "content": user_message})

        #Starts timing for response time data
        start_time = time.time()

        completion = client.chat.completions.create(
            model=selected_model,
            messages=conversation
        )
        response = completion.choices[0].message.content

        #Ends timing for response time data
        end_time = time.time()
        response_time = end_time - start_time

        total_time += response_time
        times_chatted += 1

        print(f"AI: {response}\n")
        conversation.append({"role": "assistant", "content": response})
    
    # Calculate average response time
    avg_run = total_time / times_chatted if times_chatted > 0 else 0

    review_question = input("Would you like to leave a review for this model? (y/n): ")
    if review_question.strip().lower() == 'y':
        ratings = input("Please rate the model from 1 to 10: \n")
        review = input("Please enter a review: \n")
        print("Thank you for your review!\n")

        conn = sqlite3.connect('review_data.db')
        cursor = conn.cursor()

        match choice:
            case "1":
                cursor.execute('''
                    INSERT INTO Deepseek (ratings, review, avg_run)
                    VALUES (?, ?, ?)
                ''', (ratings, review, avg_run))

                #close connection
                conn.commit()
                conn.close()
                pass
            case "2":
                cursor.execute('''
                    INSERT INTO MetaLlama (ratings, review, avg_run)
                    VALUES (?, ?, ?)
                ''', (ratings, review, avg_run))

                #close connection
                conn.commit()
                conn.close()
                pass
            case "3":
                cursor.execute('''
                    INSERT INTO MistralAI (ratings, review, avg_run)
                    VALUES (?, ?, ?)
                ''', (ratings, review, avg_run))
                #close connection
                conn.commit()
                conn.close()
                pass
        


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