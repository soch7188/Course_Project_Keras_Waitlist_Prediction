#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import menu_1
 
# Main definition - constants
menu_actions  = {}  
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    
    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Collection Dropping and Empty Collection Creating")
    print("2. Data Crawling")
    print("3. Course Search")
    print("4. Waiting List Size Prediction")
    print("5. Waiting List Size Training")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
    return
 
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
 
# Menu 1
# def menu1():
#     exec_menu(choice)
#     return
 
 
# Menu 2
def menu2():
    print("Hello Menu 2 !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

# Menu 3
def menu3():
    print("Hello Menu 3 !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

# Menu 4
def menu4():
    print("Hello Menu 4 !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

# Menu 5
def menu5():
    print("Hello Menu 5 !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
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
    '1': menu_1.run,
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