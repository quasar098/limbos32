from os import system
from _thread import start_new_thread
from time import sleep
from json import loads, dumps, load

counted = 0

# configurables (do config.json)
py = "python3"
# ==============================

try:
    with open("config.json") as f:
        data: dict[str, any] = load(f)
        py = data.get("py", "python3")
except FileNotFoundError:
    pass

def threadeded():
    global counted
    system(py + " main.py")
    counted -= 1


for _ in range(8):
    counted += 1
    start_new_thread(threadeded, ())
    sleep(0.23)

while counted:
    sleep(0.1)
