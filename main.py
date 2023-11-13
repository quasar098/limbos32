import socket
import pygame
# noinspection PyUnresolvedReferences,PyProtectedMember
from pygame._sdl2 import Window
from typing import Any
from _thread import start_new_thread
import winsound
from time import sleep
from json import loads, dumps, load
from pymsgbox import alert


class LimboKeysClient:
    def __init__(self):
        self.id = -1  # 0-7 assigned by server, -1 if unknown
        self.position = [0, -300]
        self.id_surface = pygame.Surface((0, 0))
        self.wants_to_quit = False
        self.alive = True
        self.highlight_amount: float = 0
        self.clicked = False
        self.success = False
        start_new_thread(self.listening_thread, ())

    def listening_thread(self):
        try:
            assigned_client_id = False
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 28954))
                s.sendall(dumps({"quit": False, "clicked": False}).encode('ascii'))
                while True:
                    sleep(0.02)
                    msg: dict[str, Any] = loads(s.recv(1024).decode('ascii'))
                    self.id = msg["id"]
                    self.position = msg["position"]
                    self.alive = msg["alive"]
                    self.success = msg["success"]
                    self.highlight_amount = min(1, max(self.highlight_amount+msg["highlight"]*4/FRAMERATE, 0))
                    if not assigned_client_id:
                        if self.id == 0:
                            pygame.mixer.music.load("LIMBO.mp3")
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play()
                            pygame.mixer.music.set_pos(176)
                        self.id_surface = font.render(str(self.id), True, (0, 0, 0))
                        assigned_client_id = True
                    s.sendall(dumps({"quit": self.wants_to_quit, "clicked": self.clicked}).encode('ascii'))
        except Exception as e:
            print(e)


WIDTH, HEIGHT, FRAMERATE = 150, 150, 75

# configurables
borderless = False
transparent = False
# =============

try:
    with open("config.json") as f:
        data: dict[str, Any] = load(f)
        borderless = data.get("borderless")
        transparent = data.get("transparent")
except FileNotFoundError:
    pass

pygame.init()
flags = 0
if borderless:
    flags |= pygame.NOFRAME

screen = pygame.display.set_mode([WIDTH, HEIGHT], flags=flags)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

key = pygame.image.load("key.png").convert_alpha()
green_key = pygame.image.load("green-key.png").convert_alpha()
pygame.display.set_caption("LIMBO")

client = LimboKeysClient()
pgwindow = Window.from_display_module()

if transparent:
    import win32api
    import win32con
    import win32gui
    # Create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(1, 1, 1)), 0, win32con.LWA_COLORKEY)

running = True
while running and client.alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.wants_to_quit = True
            sleep(0.1)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                client.clicked = True

    screen.fill((1, 1, 1))
    if client.highlight_amount != 0:
        screen.blit(green_key, green_key.get_rect(center=(WIDTH/2, HEIGHT/2)))
        key.set_alpha(255-int(client.highlight_amount*255))
        screen.blit(key, key.get_rect(center=(WIDTH/2, HEIGHT/2)))
    else:
        screen.blit(key, key.get_rect(center=(WIDTH/2, HEIGHT/2)))
    # screen.blit(client.id_surface, (10, 10))

    pgwindow.position = [int(pos) for pos in client.position]

    pygame.display.flip()
    clock.tick(FRAMERATE)
if client.clicked:
    if client.success:
        alert("You win")
    else:
        start_new_thread(winsound.PlaySound, ("SystemExclamation", winsound.SND_ALIAS))
        alert("Wrong guess")
pygame.quit()
