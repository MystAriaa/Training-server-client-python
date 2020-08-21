# client listener
import socket, select, string, sys, os, time
import sys, pygame
from module import *

pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255
green = 0, 255, 0

screen = pygame.display.set_mode(size)

screen.fill(black)

carte = Carte(5,5)
carte.load_from_json("map_save.json")

hote = "localhost"
port = 12800
	
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie\nCLIENT LISTENER\n\n----------------------------------------------\n")
	
while True:
    time.sleep(0.5)
    try:
        data = "get_map_update"
        connexion_avec_serveur.send(data.encode())
        msg = connexion_avec_serveur.recv(1024);
        msg = msg.decode()
        carte.string_to_map(msg)
    except:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for i in range(carte.dimX):
        for j in range(carte.dimY):
            if carte.map[str(j)+"/"+str(i)] == "Grass":
                pygame.draw.rect(screen,green,(i*200,j*200,200,200))
            else:
                pygame.draw.rect(screen,black,(i*200,j*200,200,200))

    pygame.display.update()