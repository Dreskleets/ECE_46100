from huggingface import select_model, chat_with_model, get_inference_client
import sqlite3, os, huggingface.py

#UI Menu Layout

#1.) Reviews
    #SQL lite (6 DB)
        #User Reviews (1-10)
        #Average Runtime (per chat)
#2.) Chat (HF)
#3.) Performance (Testing / Runtime)

#Hugging Face Menu (2)
def menu():
    print(f"Welcome to the ACME AI Database and Chat System!\nWhat would you like to do today?\n\n")
    print("1. Chat with models\n"
        "2. View model reviews\n"
        "3. View performance data\n"
        "4. Exit")
    
    choice = input("Enter your choice (1-4): ")
    
