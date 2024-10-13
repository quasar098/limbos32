import socketserver
from json import loads, dumps
from typing import Any
from time import time, sleep
from math import cos, sin, pi
from random import choice, seed
from random import randint
from json import loads, dumps, load
import os

# configurables (do config.json)
SC_WIDTH, SC_HEIGHT = -1, -1 # Detect Screen size
SPACING = 100 # Spacing (logic)
tcp_printblocking_lenght = 0.6 / 60 # Default
tickrate = 60
# ==============================

try:
    with open("config.json") as f:
        data: dict[str, Any] = load(f)
        SC_WIDTH = data.get("screen_width", -1) # -1 detects the screen size
        SC_HEIGHT = data.get("screen_height", -1) # -1 detects the screen size
        SPACING = data.get("spacing", 100)
        tickrate = data.get("tickrate", 60)
except FileNotFoundError:
    pass
except ZeroDivisionError:
    tcp_printblocking_lenght = 0
    STEP_SPEED = 0.3
tcp_printblocking_lenght = 0.6 / tickrate
if SC_WIDTH == -1 and SC_HEIGHT == -1:
    if os.name == "nt":
        from win32api import GetSystemMetrics
        SC_WIDTH, SC_HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
    else:
        import pygame
        from pygame.locals import *

        pygame.init()
        screen = pygame.display.set_mode((640,480), FULLSCREEN)
        SC_WIDTH, SC_HEIGHT = screen.get_size()
        pygame.quit()
        del(screen)
print("Screen size:" + str(SC_WIDTH) + "X" + str(SC_HEIGHT))
W_WIDTH, W_HEIGHT = 150, 150
DO_TIMES = 30

GAME_START_TIME = 5.4
STEP_SPEED = tcp_printblocking_lenght * 30 * (tickrate/60) # tcp_printblocking_lenght to STEP_SPEED

seed(0xF0C_5 + int.from_bytes(os.urandom(2), byteorder='big'))  # FOCUS

step_map = {
    0:  {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3},  # mirror across x axis
    1:  {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 0},  # move right column to left and cross
    2:  {0: 7, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6},  # move left column to right and cross
    3:  {0: 5, 1: 4, 4: 1, 5: 0, 2: 7, 3: 6, 6: 3, 7: 2},  # two x patterns
    4:  {0: 3, 1: 2, 2: 1, 3: 0, 4: 7, 5: 6, 6: 5, 7: 4},  # mirror across y axis
    5:  {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0},  # right+right stuff
    6:  {0: 1, 1: 5, 5: 4, 4: 0, 2: 3, 3: 7, 7: 6, 6: 2},  # left+left stuff
    7:  {1: 0, 5: 1, 4: 5, 0: 4, 3: 2, 7: 3, 6: 7, 2: 6},  # right+left stuff
    8:  {1: 0, 5: 1, 4: 5, 0: 4, 2: 3, 3: 7, 7: 6, 6: 2},  # left+right stuff
    9:  {0: 6, 1: 7, 2: 4, 3: 5, 4: 2, 5: 3, 6: 0, 7: 1},  # cross 2 wide blocks
    10: {0: 5, 1: 6, 2: 7, 3: 3, 4: 4, 5: 0, 6: 1, 7: 2},  # swap top left 3 and bottom right 3
    11: {0: 0, 1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3, 7: 7},  # swap top right 3 and bottom left 3
}

forbidden_pairs = [
    (10, 9),
    (11, 9),
    (9, 10),
    (9, 11),
    (1, 2),
    (2, 1)
]


def lerp(p1: list, p2: list, amt: float):
    return [p1[x] * (1 - amt) + p2[x] * amt for x in range(len(p1))]


def serp(p1: list, p2: list, amt: float):
    return lerp(p1, p2, (1-cos(amt*pi))/2)


def get_static_pos(client_id: int):
    return [
        int(SC_WIDTH / 2 - W_WIDTH * 2 - SPACING*2 + (client_id % 4) * (W_WIDTH + SPACING)),
        int(SC_HEIGHT / 2 - W_HEIGHT - SPACING + (W_HEIGHT + SPACING*2) * (client_id // 4))
    ]


def get_circle_pos(client_id: int, time_offset: float):
    return [
        int(SC_WIDTH / 2 - W_WIDTH / 2)+cos(pi*client_id/4+time_offset/2)*SC_WIDTH*2/8,
        int(SC_HEIGHT / 2 - W_HEIGHT / 2)+sin(pi*client_id/4+time_offset/2)*SC_HEIGHT*2/8
    ]


def get_pos(client_id: int, current_time: float, steps: list):

    if current_time < GAME_START_TIME:
        return get_static_pos(client_id)

    running_time = current_time - GAME_START_TIME

    completed_steps = steps[:int(running_time / STEP_SPEED)]
    try:
        current_step = steps[int(running_time / STEP_SPEED)]
    except IndexError:
        current_step = None

    spoofed_id = client_id
    for step in completed_steps:
        spoofed_id = step_map[step][spoofed_id]
    if current_step is None:
        lerped = max(0.0, min(1.0, (current_time - GAME_START_TIME - STEP_SPEED * DO_TIMES) / 2))
        lerped = 1 + pow(lerped-1, 3)
        return lerp(get_static_pos(spoofed_id), get_circle_pos(client_id, current_time), lerped)
    lerped = serp(
        get_static_pos(spoofed_id),
        get_static_pos(step_map[current_step][spoofed_id]),
        (running_time / STEP_SPEED) % 1)
    # print(spoofed_id, step_map[current_step][spoofed_id])
    return lerped


class TCPHandler(socketserver.BaseRequestHandler):
    clients = []
    start_time = 0
    steps = []
    correct_key = -1
    alive = True
    success = False
    print_blocking = False

    def handle(self) -> None:
        if len(TCPHandler.clients) >= 8:
            return
        if not TCPHandler.alive:
            return
        client_id = 0
        while True:
            if client_id not in TCPHandler.clients:
                break
            client_id += 1
        TCPHandler.clients.append(client_id)
        if client_id == 0:
            TCPHandler.steps = []
            prev_move = -1
            for _ in range(DO_TIMES):
                move = -1
                while prev_move == move or move == -1:
                    move = choice(list(step_map.keys()))
                    if len(TCPHandler.steps) and (TCPHandler.steps[-1], move) in forbidden_pairs:
                        move = -1
                    if len(step_map) == 1:
                        break
                TCPHandler.steps.append(move)
                prev_move = move
            TCPHandler.start_time = time()
            TCPHandler.correct_key = randint(0, 7)
        print(f"{client_id} joined")
        try:
            while True:
                TCPHandler.success = False
                data: dict[str, Any] = loads(self.request.recv(1024).decode('ascii'))
                if data["quit"]:
                    TCPHandler.alive = False
                if data["clicked"]:
                    if TCPHandler.correct_key == client_id:
                        TCPHandler.success = True
                    TCPHandler.alive = False
                current_time = time() - TCPHandler.start_time
                reply = {
                    "id": client_id,
                    "position": get_pos(client_id, current_time, TCPHandler.steps),
                    "alive": TCPHandler.alive,
                    "highlight": 1 if client_id == TCPHandler.correct_key and 2 < current_time < 3 else -1,
                    "success": TCPHandler.success,
                    "clickable": current_time > GAME_START_TIME+STEP_SPEED*DO_TIMES+0.5,
                    "movement_finished": current_time > GAME_START_TIME+STEP_SPEED*DO_TIMES,
                }
                reply = dumps(reply).encode('ascii')
                self.request.sendall(reply)
        except OSError:
            pass
        finally:
            while TCPHandler.print_blocking:
                sleep(tcp_printblocking_lenght)
            TCPHandler.print_blocking = True
            print(f"{client_id} left")
            TCPHandler.print_blocking = False
            if len(TCPHandler.clients) == 1:
                TCPHandler.alive = True
                print("======================")
            TCPHandler.clients.remove(client_id)


def main():
    host, port = "localhost", 6666

    with socketserver.ThreadingTCPServer((host, port), TCPHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
