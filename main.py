'''
Author: Rachel Robins
Updated: 6/14/23
Description: This program runs the virtual assistant "Aida" who will
execute tasks according to the user's input.
'''
from datetime import date
import time

USER_NAME = 'Friend'
END_WORDS = ['quit', 'stop', 'bye']

def welcome():
    '''
    Prints a welcome message for the user upon running the program
    '''
    print(f'Welcome back, {USER_NAME}!')
    
def get_date():
    '''
    Prints the current date textually using the datetime module
    '''
    today = date.today().strftime("%B %d, %Y")
    print(f'Today\'s date is: {today}')
    
def get_time():
    '''
    Prints the current local time formatted as a string using the time module
    '''
    now = time.localtime()
    current_time = time.strftime('%H:%M:%S', now)
    print(current_time)

    

if __name__ == "__main__":
    welcome()
    
    while True:
        command = input().lower()
        
        if "date" in command:
            get_date()
        elif any(word in command for word in END_WORDS):
            print(f'Goodbye, {USER_NAME}!')
            break