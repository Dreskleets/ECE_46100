import os, sqlite3

def main_menu():
    print("Which model would you like to see?\n\n")
    print("1. Deepseek\n"
          "2. MetaLlama\n"
          "3. MistralAI\n"
          "4. Exit")
    
    choice = input("Enter your choice (1-4): ")

    match choice:
        case "1": 
            AI_name = "Deepseek"
            review_menu(AI_name)
            pass
        case "2":
            AI_name = "MetaLlama"
            review_menu(AI_name)
            pass
        case "3":
            AI_name = "MistralAI"
            review_menu(AI_name)
            pass
        case "4":
            print("Exiting the program. Goodbye!")
            return(False)
        case _:
            print("Invalid choice. Please enter a number between 1 and 2.\n\n\n\n")
            return(True)

def review_menu(AI_name):
    # This will act as a template to show reviews for each model
    # AI_name is used to access the correct database table

    review_menu_exit = input("Press enter to return to menu")

    if review_menu_exit:
        return



exit = True

def main():
    while exit == True:
        exit = main_menu()
