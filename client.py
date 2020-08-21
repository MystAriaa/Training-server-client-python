import socket
import json
import os
import sys
import select
from module import *


hote = "localhost"
port = 12800

client_running = True
server_restart = False

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

#thread_check_connection = Check_Connection_Client(connexion_avec_serveur)
#thread_check_connection.start()

msg_a_envoyer = b""
while client_running:
    
    msg_a_envoyer = input("> ")
    connexion_avec_serveur.send(msg_a_envoyer.encode())
    msg_recu = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode()

    if (msg_a_envoyer == "show"):
        data = json.loads(msg_recu)

    elif (msg_a_envoyer == "/stop"):
        client_running = False

    elif (msg_a_envoyer == "/disconnect"):
        client_running = False

    elif (msg_a_envoyer == "/restart"):
        data = msg_recu
        client_running = False
        server_restart = True

    else:
        data = msg_recu

    try:
        print(data)
    except:
        pass


print("Fermeture de la connexion")
try:
    connexion_avec_serveur.close()
except:
    pass

if server_restart:
    os.system('python client.py')

sys.exit()