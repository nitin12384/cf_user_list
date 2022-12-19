
import time

def error(msg:str):
    print("Error - " + msg)

def log(msg:str):
    print("Log - " + msg)

def debug(msg : str):
    print("[" + time.asctime() + "] " + msg )
