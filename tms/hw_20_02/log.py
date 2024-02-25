import os, time, psutil

def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')
        












while True:
