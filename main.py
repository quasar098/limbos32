import sys, os
from os import system
from _thread import start_new_thread
from time import sleep

counted = 0
start_new_thread(os.system, (f'"{sys.executable}" server.py',))

def threadeded():
    global counted
    os.system(f'"{sys.executable}" client.py')
    counted -= 1


for _ in range(8):
    counted += 1
    start_new_thread(threadeded, ())
    sleep(0.23)

while counted:
    sleep(0.1)
