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
    print("Hi thank you for using our product!")
    choice_2 = input("Would you like to leave a in depth review over the program? (y/n):")
    match choice_2:
        case "y":
            open_source_review()
        case "n":
            return_to_admin_menu()
        case _:
            return(True)    
        
def open_source_review():
    print("Welcome to the review menu!")
    ramp_up_time_metric = input("Please rate your overall experience from downloading the product to full usability (1-10):")
    rating_check(ramp_up_time_metric)
    print("Thank You!")
    bus_factor_metric = input("Please rate how well you would be able to begin working on this project if we were to lose a developer (1-10):")
    rating_check(bus_factor_metric)
    print("Thank You!")
    license_metric = input("Please rate how well our licensing documentation and usage was (1-10):")
    rating_check(license_metric)
    print("Thank You!")
    size_score_metric = input("Please rate the size and portability of our program (1-10):")
    rating_check(size_score_metric)
    print("Thank You!")
    data_score_metric = input("Please rate the availability and quality of our data (1-10):")
    rating_check(data_score_metric)
    print("Thank You!")
    code_quality_metric = input("Please rate the quality, maintainability, and reliability of our code (1-10):")
    rating_check(code_quality_metric)
    print("Thank you for leaving us a review today!")
    net_score_avg = ((int(ramp_up_time_metric)) 
                     + (int(bus_factor_metric)) 
                     + (int(license_metric)) 
                     + (int(size_score_metric)) 
                     + (int(data_score_metric)) 
                     + (int(code_quality_metric))) / 6
    print("Your review has a net score of", net_score_avg)
    unhappy_metric = input("Would you like to keep this metric? (y/n):")
    match unhappy_metric:
        case "y":
            print("Great! Thank you again :)")
            return_to_admin_menu()
        case "n":
            print("Thank you! Now resetting metrics for a new review", end = " ", flush = True)
            time.sleep(0.5)
            print(".", end = " ", flush = True)
            time.sleep(0.5)
            print(".", end = " ", flush = True)
            time.sleep(0.5)
            print(".")
            time.sleep(0.5)
            open_source_review()
        case _:
            print("Invalid Response. Please enter either y or n")
            return(False)
def ai_performance_menu():
    #Delete function contents when create actual functions
    #Want to have a quick summary of the AI and what the average runtime from our database is
    return_to_admin_menu()
    
def lines_of_code_report():
    #Full Report of lines of code for all files and a total LOC
    #Delete function contents when create actual functions
    return_to_admin_menu()
    
def licenses_menu():
    #License database and information menu
    #Delete function contents when create actual functions
    return_to_admin_menu()
    
def net_score_menu():
    #Similar to AI performance menu except with the average net score for each one
    #Delete function contents when create actual functions
    return_to_admin_menu()
    
#Quick function for a clean exit
def return_to_admin_menu():
    print("Thank you! Now returning to menu", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".", end = " ", flush = True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    admin_menu()
    
#Function to check whether a number is between 1 and 10
def rating_check(rating_metric):
    check = True
    while check:
        if int(rating_metric) >= 1 and int(rating_metric) <= 10:
            return(rating_metric)
        else:
            rating_metric = input("Please enter a valid number 1-10: ")
        
    
    