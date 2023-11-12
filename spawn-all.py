from os import system
from _thread import start_new_thread
from time import sleep
from pymsgbox import alert


counted = 0


def threadeded():
    global counted
    counted += 1
    system("python3 main.py")
    counted -= 1


for _ in range(8):
    start_new_thread(threadeded, ())
    sleep(0.2)

while counted:
    sleep(0.1)
