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

import UI, time, sqlite3, os

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
    
    conn = sqlite3.connect('review_data.db')
    cursor = conn.cursor()
    
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
    cursor.execute('''
                INSERT INTO NetScore (net_score, ramp_up_time_metric, bus_factor_metric, license_metric, size_score_metric, data_score_metric, code_quality_metric)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (net_score_avg, ramp_up_time_metric, bus_factor_metric, license_metric, size_score_metric, data_score_metric, code_quality_metric))
    conn.commit()
    conn.close()
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
    conn = sqlite3.connect('review_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT AVG(avg_run) FROM DeepSeek")
    deepseek_avg_run = cursor.fetchone()[0]
    cursor.execute("SELECT avg_run FROM DeepSeek ORDER BY id DESC LIMIT 5")
    deepseek_last_5 = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT AVG(avg_run) FROM MetaLlama")
    metallama_avg_run = cursor.fetchone()[0]
    cursor.execute("SELECT avg_run FROM MetaLlama ORDER BY id DESC LIMIT 5")
    metallama_last_5 = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT AVG(avg_run) FROM MistralAI")
    mistral_avg_run = cursor.fetchone()[0]
    cursor.execute("SELECT avg_run FROM MistralAI ORDER BY id DESC LIMIT 5")
    mistral_last_5 = [row[0] for row in cursor.fetchall()]
    
    print("Performance Statistics")
    print("---------------------")
    print("  Average Runtimes")
    print("  DeepSeek || MetaLlama || MistralAi")
    print("   ",f"{deepseek_avg_run:.2f}","      ", f"{metallama_avg_run:.2f}","       ", f"{mistral_avg_run:.2f}")
    print("---------------------")
    print("  Last 5 Runtimes ")
    print("  DeepSeek  ")
    print([f"{score:.2f}" for score in deepseek_last_5])
    print("  MetaLlama  ")
    print([f"{score:.2f}" for score in metallama_last_5])
    print("  Mistral  ")
    print([f"{score:.2f}" for score in mistral_last_5])
    print("---------------------")
    cursor.close()
    
    time.sleep(1)
    
    choice = input("Would you like to return to the menu? (y/n): ")
    match choice:
        case "y":
            return_to_admin_menu()
        case "n":
            ai_performance_menu()
        case _:
            print("Please enter either y or n")
    
def lines_of_code_report(directory = "."):
    total_lines = 0
    
    print(" Python Files Total Lines of Code")
    print("----------------------------------")
    #Used Chat GPT Prompt "How would i create a function for say an admin menu that will be able to tell me the 
    #total lines of code without comments or blank lines through each file and the whole file combined for python files?"
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    line_count = 0
                    for line in f:
                        stripped = line.strip()
                        # Skip empty lines and comment lines
                        if stripped and not stripped.startswith("#"):
                            line_count += 1

                total_lines += line_count
                print(f"{file_path}: {line_count} lines")

    print("-" * 50)
    print(f"TOTAL: {total_lines} lines across all Python files")
    
    time.sleep(1)
    
    choice = input("Would you like to return to the menu? (y/n): ")
    match choice:
        case "y":
            return_to_admin_menu()
        case "n":
            lines_of_code_report()
        case _:
            print("Please enter either y or n")
    
def licenses_menu():
    conn = sqlite3.connect('review_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT license_name FROM Licenses ORDER BY id")
    license_list = [row[0] for row in cursor.fetchall()]
    
    print("    License Menu     ")
    print("---------------------")
    for license_list in license_list:
        print(license_list)
    print("---------------------")
    
    cursor.close()
    
    time.sleep(1)
    
    choice = input("Would you like to return to the menu? (y/n): ")
    match choice:
        case "y":
            return_to_admin_menu()
        case "n":
            net_score_menu()
        case _:
            print("Please enter either y or n")
    
    
def net_score_menu():
    
    conn = sqlite3.connect('review_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT AVG(net_score) FROM NetScore")
    net_score_avg = cursor.fetchone()[0]
    cursor.execute("SELECT net_score FROM NetScore ORDER BY id DESC LIMIT 5")
    last_5 = [row[0] for row in cursor.fetchall()]
    
    print("Net Score Statistics")
    print("---------------------")
    print("  Net Score Average")
    print("       ",f"{net_score_avg:.2f}")
    print("---------------------")
    print("  Last 5 Net Scores")
    print([f"{score:.2f}" for score in last_5])
    print("---------------------")
    
    cursor.close()
    
    time.sleep(1)
    
    choice = input("Would you like to return to the menu? (y/n): ")
    match choice:
        case "y":
            return_to_admin_menu()
        case "n":
            net_score_menu()
        case _:
            print("Please enter either y or n")
    
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
        
    
    