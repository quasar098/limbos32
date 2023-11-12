import socket

import pygame
# noinspection PyUnresolvedReferences,PyProtectedMember
from pygame._sdl2 import Window
from typing import Any
from _thread import start_new_thread
from time import sleep
from json import loads, dumps


class LimboKeysClient:
    def __init__(self):
        self.id = -1  # 0-7 assigned by server, -1 if unknown
        self.position = [0, -300]
        self.id_surface = pygame.Surface((0, 0))
        self.wants_to_quit = False
        start_new_thread(self.listening_thread, ())

    def listening_thread(self):
        assigned_client_id = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 6666))
            s.sendall(dumps({"quit": False}).encode('ascii'))
            while True:
                sleep(0.02)
                msg: dict[str, Any] = loads(s.recv(1024).decode('ascii'))
                self.id = msg["id"]
                self.position = msg["position"]
                if not assigned_client_id:
                    if self.id == 0:
                        pygame.mixer.music.load("LIMBO.mp3")
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_pos(178)
                    self.id_surface = font.render(str(self.id), True, (0, 0, 0))
                    assigned_client_id = True
                s.sendall(dumps({"quit": self.wants_to_quit}).encode('ascii'))


WIDTH, HEIGHT, FRAMERATE = 260, 260, 75

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

key = pygame.image.load("key.png").convert_alpha()
pygame.display.set_caption("LIMBO")

BG_COLOR = pygame.Color(190, 190, 190)

client = LimboKeysClient()
pgwindow = Window.from_display_module()

running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.wants_to_quit = True
            sleep(0.1)
            running = False

    pgwindow.position = [int(pos) for pos in client.position]

    screen.blit(key, key.get_rect(center=(WIDTH/2, HEIGHT/2)))
    screen.blit(client.id_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
