import socket
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
del os
# noinspection PyUnresolvedReferences,PyProtectedMember
from pygame._sdl2 import Window
from typing import Any
from _thread import start_new_thread
import winsound
from time import sleep
from json import loads, dumps, load
from pymsgbox import alert

# configurables (do config.json)
borderless = False # Disable borders
transparent = False # Transparency
music = True # Music (handled by client 0)
sfx = True # SFX (handled by client 0)
fps = 75 # FPS
volume = 0.3 # Volume of the music (handled by client 0)
smoothness = 0.03 # How much time should be the client waiting, lower this for larger smoothness
connection_port = 6666 # Port to connect to
client_scale_x = 150 # Width of the client
client_scale_y = 150 # Height of the client
use_texture_pack = False # Use the folder "textures" for the images
double_show = False # Funny way of showing both images at once
always_show_key = False # Always show the correct key
loop_music = False # Loop the music (handled by client 0)
client_server_ip = "localhost" # The IP of the server
# ==============================

try:
    with open("config.json") as f:
        data: dict[str, Any] = load(f)
        borderless = data.get("borderless", False)
        transparent = data.get("transparent", False)
        music = data.get("music", True)
        sfx = data.get("sfx", True)
        fps = data.get("fps", 75)
        volume = data.get("volume", 0.3)
        smoothness = data.get("smoothness", 0.03)
        connection_port = data.get("connection_port", 6666)
        use_texture_pack = data.get("use_texture_pack", False)
        double_show = data.get("double_show", False)
        always_show_key = data.get("always_show_key", False)
        loop_music = data.get("loop_music", False)
        client_scale_x = data.get("client_scale_x", 150)
        client_scale_y = data.get("client_scale_y", 150)
        client_server_ip = data.get("client_server_ip", "localhost")
except FileNotFoundError:
    pass

class LimboKeysClient:
    def __init__(self):
        self.id = -1  # 0-7 assigned by server, -1 if unknown
        self.position = [0, -300]
        self.id_surface = pygame.Surface((0, 0))
        self.wants_to_quit = False
        self.alive = True
        self.highlight_amount: float = 0
        self.clicked = False
        self.clickable = False
        self.success = False
        start_new_thread(self.listening_thread, ())

    def listening_thread(self):
        try:
            self.has_been_looped = False
            assigned_client_id = False
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((client_server_ip, connection_port))
                s.sendall(dumps({"quit": False, "clicked": False}).encode('ascii'))
                while True:
                    sleep(smoothness)
                    msg: dict[str, Any] = loads(s.recv(1024).decode('ascii'))
                    self.id = msg["id"]
                    self.position = msg["position"]
                    self.alive = msg["alive"]
                    self.success = msg["success"]
                    self.clickable = msg["clickable"]
                    self.highlight = msg["highlight"]
                    if self.id == 0:
                        if loop_music:
                            if self.has_been_looped:
                                on_time_loop = 5000
                            else:
                                on_time_loop = 20000
                            if pygame.mixer.music.get_pos() >= on_time_loop:
                                pygame.mixer.music.stop()
                                pygame.mixer.music.play()
                                pygame.mixer.music.set_pos(193)
                                self.has_been_looped = True

                    if double_show:
                        self.highlight_amount = msg["highlight"]
                    if always_show_key:
                        self.highlight_amount = min(4, max(self.highlight_amount + msg["highlight"] * 4, 0))
                    if not always_show_key and not double_show:
                        self.highlight_amount = min(1, max(self.highlight_amount + msg["highlight"] * 4 / FRAMERATE, 0))
                    if not assigned_client_id:
                        if self.id == 0:
                            if music:
                                pygame.mixer.music.load("LIMBO.mp3")
                                pygame.mixer.music.set_volume(volume)
                                pygame.mixer.music.play()
                                pygame.mixer.music.set_pos(176)
                        self.id_surface = font.render(str(self.id), True, (0, 0, 0))
                        assigned_client_id = True
                    s.sendall(dumps({"quit": self.wants_to_quit, "clicked": self.clicked}).encode('ascii'))
        except Exception as e:
            print(e)

WIDTH, HEIGHT, FRAMERATE = client_scale_x, client_scale_y, fps

pygame.init()
flags = 0
if borderless:
    flags |= pygame.NOFRAME

screen = pygame.display.set_mode([WIDTH, HEIGHT], flags=flags)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

if use_texture_pack:
    prefix_key_path = "textures\\"
else:
    prefix_key_path = ""
key = pygame.image.load(prefix_key_path + "key.png").convert_alpha()
green_key = pygame.image.load(prefix_key_path + "green-key.png").convert_alpha()
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
                if client.clickable:
                    client.clicked = True

    screen.fill((1, 1, 1))
    if client.highlight_amount != 0:
        screen.blit(green_key, green_key.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        key.set_alpha(255 - int(client.highlight_amount * 255))
        screen.blit(key, key.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
    else:
        screen.blit(key, key.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
    # screen.blit(client.id_surface, (10, 10))

    pgwindow.position = [int(pos) for pos in client.position]

    pygame.display.flip()
    clock.tick(FRAMERATE)
if client.clicked:
    if client.success:
        alert("You win", "Win")
    else:
        if sfx:
            start_new_thread(winsound.PlaySound, ("SystemExclamation", winsound.SND_ALIAS))
        alert("Wrong guess", "Wrong")
pygame.quit()
