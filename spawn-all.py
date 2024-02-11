from shutil import which
from os import system
from _thread import start_new_thread
from time import sleep

python_path = which("python")
python3_path = which("python3")
if (python3_path is None) or (python_path and (("WindowsApps" in python3_path) or ("mingw64" in python3_path))):
    cmd = "python"
else:
    cmd = "python3"

counted = 0
def threadeded():
    global counted
    system(cmd+" main.py")
    counted -= 1
for _ in range(8):
    counted += 1
    start_new_thread(threadeded, ())
    sleep(0.23)
while counted:
    sleep(0.1)
