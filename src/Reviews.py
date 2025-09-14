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
        case "2":
            AI_name = "MetaLlama"
            review_menu(AI_name)
        case "3":
            AI_name = "MistralAI"
            review_menu(AI_name)
        case "4":
            print("Exiting the program. Goodbye!")
            return(False)
        case _:
            print("Invalid choice. Please enter a number between 1 and 2.\n\n\n\n")
            return(True)

def review_menu(AI_name):
    # This will act as a template to show reviews for each model
    # AI_name is used to access the correct database table

    conn = sqlite3.connect('review_data.db')
    cursor = conn.cursor()
    match AI_name:
        case "Deepseek":
            cursor.execute('SELECT review, ratings FROM Deepseek')
            reviews = cursor.fetchall()
            print("\nReviews and Ratings:\n")
            for review in reviews:
                print(review)
        case "MetaLlama":
            cursor.execute('SELECT review, ratings FROM MetaLlama')
            reviews = cursor.fetchall()
            print("\nReviews and Ratings:\n")
            for review in reviews:
                print(review)
        case "MistralAI":
            cursor.execute('SELECT review, ratings FROM MistralAI')
            reviews = cursor.fetchall()
            print("\nReviews and Ratings:\n")
            for review in reviews:
                print(review)
    conn.close()
    input("Press enter to return to menu")



exit = True

def main():
#Didnt know what this function was doing because it caused error
#    while exit == True:
#        exit = main_menu()

#Takes you to the main_menu() if wanting options for multiple 
#reviews need implementation later
    main_menu()