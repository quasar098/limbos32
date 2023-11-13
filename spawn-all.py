from os import system
from _thread import start_new_thread
from time import sleep


counted = 0



def threadeded():
    global counted
    counted += 1
    system("python main.py")
    counted -= 1

def startserver():
    system("python server.py")

for _ in range(8):
    start_new_thread(threadeded, ())
    start_new_thread(startserver, ())
    sleep(0.23)

while counted:
    sleep(0.1)
