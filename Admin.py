#Scoring Metrics (With Latency):
#Ramp Up Time
#Bus Factor
#License Compatibility
#Size Score
#Dataset & Code Availability
#Dataset Quality
#Code Quality
#Performance Claims

#Make a file for user to rate the AI after they use it and add it to database.
#Have both the runtime and user ratings stored after exiting the chat.

#Ramp up time from start to go to menu -> select ai -> download ai -> begin chat with ai locally
#Also looking at program startup -> select ai -> begin chat with ai virtually through HF

#Bus Factor is how well could the team recoup if we lost a valuable member of the team who created for example the whole database code
#and suddenly dissapeared / was unable to contribute any information
#Complexity & Documentation of the code base

#License Compatibility is the legality of distrubuting the program with the combined program licenses (SQLite for example)

#Size score is the measurement of size (Lines of Code, Function Points, or Use Case Points, etc.)

#A Data Availability Statement is provided with detailed enough information such that an independent researcher can replicate 
#the steps needed to access the original data, including any limitations and the expected monetary and time cost of data access.

#Dataset Quality is the overall Accuracy, Completeness, Consistency, and Valid Data within a dataset.

#Code quality is the overall Maintanability, readability, reliability, and security of the code base

#Use a net score to validate these metrics into a single metric.

import UI, time

def admin_access():
    print("Welcome to the Admin Menu:")
    choice_1 = input("Login? (y/n):")
    #Admin User & Pass check 
    match choice_1:
        case "y" | "Y":
            print("Please enter the Admin Username\n")
            AdminUser = input("Username:")
            print("Please enter the Admin Password\n")
            AdminPass = input("Password:")
            if AdminUser == "admin":
                if AdminPass == "pass":
                    admin_menu()
        case "n" | "N":
            UI.menu()
        case "q":
            print("Exiting the program. Goodbye")
        case _:
            print("Invalid choice. Please enter either y or n")
            return(True)
        
def admin_menu():
    print("Hi welcome to the Admin Menu\n")
    print("What would you like to access today?\n"
          "1.)Open Source User Rating Menu\n"
          "2.)Performance of AI\n"
          "3.)Lines of Code Report\n"
          "4.)Licenses\n"
          "5.)Net Score Calculator\n"
          "6.)Exit\n")
    choice = input("Please enter your choice (1-6): ")
    match choice:
        case "1":
            open_source_menu()
        case "2":
            ai_performance_menu()
        case "3":
            lines_of_code_report()
        case "4":
            licenses_menu()
        case "5":
            net_score_menu()
        case "6":
            return(False)
    
def open_source_menu():
    print("Work in progress. Returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()
def ai_performance_menu():
    print("Work in progress. Returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()
def lines_of_code_report():
    print("Work in progress. Returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()
def licenses_menu():
    print("Work in progress. Returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()
def net_score_menu():
    print("Work in progress. Returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()