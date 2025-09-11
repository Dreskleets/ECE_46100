import huggingface, Reviews
import sqlite3, os


#UI Menu Layout

#1.) Reviews
    #SQL lite (6 DB)
        #User Reviews (1-10)
        #Average Runtime (per chat)
#2.) Chat (HF)
#3.) Performance (Testing / Runtime)

#Hugging Face Menu (2)
def menu():
    print("Welcome to the ACME AI Database and Chat System!\nWhat would you like to do today?\n\n")
    print("1. Chat with models\n"
        "2. View model reviews\n"
        "3. View performance data\n"
        "4. Exit")
    
    choice = input("Enter your choice (1-4): ")

    match choice:
        case "1": 
            huggingface.huggingface_main()
            pass
        case "2":
            Reviews.main()
            pass
        case "3":
            #Performance main function goes here?
            pass
        case "4":
            print("Exiting the program. Goodbye!")
            exit()
        case _:
            print("Invalid choice. Please enter a number between 1 and 4.\n\n\n\n")

if __name__ == "__main__":
    while True:
        menu()
    
