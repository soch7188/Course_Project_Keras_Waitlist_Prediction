#team_no         :29
#title           :main.py
#description     :This program displays an interactive menu on CLI
#author          :Kim Ziwon(20216497), Hu Yao-Chieh (20216239)
#phase           :1
#version         :0.1
#usage           :python3 menu.py
#notes           :
#python_version  :3.6.3  
#mongodb_version :3.4.10 
#keras_version   :2.1.1  
#tf_version      :1.5.0rc0  
#=======================================================================

# Import the modules needed to run the script.
import sys, os

# Import menu components
import pymongo

import menu_1,menu_2,menu_3,menu_4,menu_5

# Import Python-MongoDB component
# Remember to start the MongoDB server before running this Python script
from pymongo import MongoClient
# from datetime import *


# Try to insert a document
def insertDocument(db):
    try:
        db.course.insert({
            "cid": "COMP 1001",
            "cname": "Exploring Multimedia and Internet Computing",
            "category": "COMP",
            "credit": 3,
            "courseInfo": 
            {
                "attributes": 
                [
                    "Common Core (S&T) for 2010 & 2011 3Y programs",
                    "Common Core (S&T) for 2012 3Y programs",
                    "Common Core (S&T) for 4Y programs"
                ],
                "exclusion": "ISOM 2010, any COMP courses of 2000-level or above",
                "description": "This course is an introduction to computers and computing tools. It introduces the organization and basic working mechanism of a computer system, including the development of the trend of modern computer system. It covers the fundamentals of computer hardware design and software application development. The course emphasizes the application of the state-of-the-art software tools to solve problems and present solutions via a range of skills related to multimedia and internet computing tools such as internet, e-mail, WWW, webpage design, computer animation, spread sheet charts/figures, presentations with graphics and animations, etc. The course also covers business, accessibility, and relevant security issues in the use of computers and Internet."
            },      
            "sectionList":
            [
                {
                    "section": "L1",
                    "sectionNumber": 1756,
                    "dateTime": 
                    {

                        "weekDay": "Thursday",
                        "startTime": "03:00PM",
                        "endTime": "04:50PM",
                    },
                    "room": "Rm 5620, Lift 31-32 (70)",
                    "instructor": "LEUNG, Wai Ting",
                    "quota": 67,
                    "enrol": 4,
                    "avail": 63,
                    "wait": 0,
                    "remarks": "",
                    "timeRecord": "25 January 2018, 09:00"
                },
                {
                    "section": "LA1",
                    "sectionNumber": 1757,
                    "dateTime": 
                    {

                        "weekDay": "Tuesday",
                        "startTime": "03:00PM",
                        "endTime": "04:50PM",

                    },
                    "room": "Rm 4210, Lift 19 (67)",
                    "instructor": "LEUNG, Wai Ting",
                    "quota": 67,
                    "enrol": 4,
                    "avail": 63,
                    "wait": 0,
                    "remarks": "",
                    "timeRecord": "25 January 2018, 09:00"
                }
            ]
        })
    except pymongo.errors.ConnectionFailure as error: 
        print("Document Insertion Failed! Error Message: \"{}\"".format(error))


def queryDocument(db, keyword):
    try:
        db.course.find({
            # "cname": {$regex: /Computer/}}
        })
    except pymongo.errors.ConnectionFailure as error: 
        print("Document Query Failed! Error Message: \"{}\"".format(error))



# Main definition - constants
menu_actions  = {}  
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():

    try:
        os.system('clear')

        # Making a DB connection
        print("Making a MongoDB connection...")
        client = MongoClient("mongodb://localhost:27017")

        # Getting a Database named "university"
        print("Getting a database named \"university\"")
        db = client["university"]
        # print(db.getCollectionNames())

        queryDocument(db, "COMP")

        print("Welcome,\n")
        print("Please choose the menu you want to start by entering the number:")
        print("(1) Collection Dropping and Empty Collection Creating")
        print("(2) Data Crawling")
        print("(3) Course Search")
        print("(4) Waiting List Size Prediction")
        print("(5) Waiting List Size Training")
        print("\n(0) Quit")
        choice = input(" >>  ")
        exec_menu(choice)

        # Closing a DB connection
        print("Closing a DB connection...")
        client.close()

        return

    except pymongo.errors.ConnectionFailure as error:
        print("DB Connection Failed! Error Message: \"{}\"".format(error))
 
# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


# Execute Menu [Post]
def exec_menu_post():
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
# Menu 1
def menu1():
    menu_1.run()

    exec_menu_post()
    return
 
 
# Menu 2
def menu2():
    menu_2.run()

    exec_menu_post()
    return

# Menu 3
def menu3():
    menu_3.run()

    exec_menu_post()
    return

# Menu 4
def menu4():
    menu_4.run()

    exec_menu_post()
    return

# Menu 5
def menu5():
    menu_5.run()

    exec_menu_post()
    return
 
# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()
 
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '9': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()



