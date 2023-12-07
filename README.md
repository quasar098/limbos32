# FOCUS

![new4](https://github.com/quasar098/limbos32/assets/70716985/36bfe28d-9616-4ee0-bc10-96d762f61105)

**NOTE: CURRENTLY ONLY WORKING ON WINDOWS 10/11**

**DO NOT LEAVE ME YOUTUBE COMMENTS ASKING ME HOW TO INSTALL THIS GAME**

## rudimentary install guide

1) install python from python.org, preferably python 3.9 or above. if you are installing it then make sure to check the box to install pip when it asks you during the install process. also check the box to set up the `PATH` environment variable or whatever and restart your pc if necessary
2) make sure python works from the terminal by going into command prompt and typing `python` (if it doesn't work, try `python3`). if it doesn't work no matter what you try, try adding python to environment path (google how to do that)
3) once you have that working, close the terminal and download the source code in github.com by clicking on the green `<> code` button and clicking "download ZIP"
4) unzip the file from file explorer or whatever
5) navigate to the unzipped folder with the source code
6) open up a new command prompt (type `cmd` in taskbar) and navigate to the directory with the source by using the `cd` and `dir` commands. most likely it will be in `C:\Users\<username>\Downloads` or something. install the dependencies by typing in `python3 -m pip install -r requirements.txt` in the command prompt. if it doesn't work, you may have to try using `python` instead of `python3`. keep that terminal open for now
7) i think double clicking on the "server.py" should run it. the server.py is always required in the background because it manages the positions and synchronization for all the windows of the limbo key game
8) in the terminal from before, type something like `python3 "spawn-all.py"`. if it doesn't work, try changing `python3` to `python`. additionally, it might not open any windows, in which case you should change `python3` to `python` in the source code in spawn-all.py

### need tech support?

if you are struggling to install this, make a github issue and someone who knows what they are doing may help you. this may or may not be me (probably not me, i don't have that much free time). if you know what you are doing and want to help others, then please answer people's questions in the github issues and i will try to mark them as resolved.
