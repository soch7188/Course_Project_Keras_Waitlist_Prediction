import os

def run():
    # Welcome message
    print("(3) Course Search\n")

    print("Please choose the menu you want to start by entering the number")
    print("[1] Course Search by Keyword")
    print("[2] Course Search by Waiting List Size")
    choice = input(" >>  ")
    exec_menu(choice)


    # Main execution
    # print("Data Crawling is successful and all data are inserted into the database")
    print("Warning: This is a stub.\n")

    return

def searchByKeyword():
    print("Course Search by Keyword...")
    return

def searchByWaitingListSize():
    print("Course Search by Keyword...")
    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()

    if ch == '1':
        searchByKeyword()
    elif ch == '2':
        searchByWaitingListSize()
    else:
        print("Please retry.")

    return
