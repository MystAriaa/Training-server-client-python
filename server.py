import socket
import select
import json
import os
from module import *

hote = ''
port = 12800

print("Initialisation de la carte ...")
carte = Carte(5,5)
try:
    carte.load_from_json("map_save.json")
    print("Map found\nLoading map ...")
    carte.determine_dimensions()
except:
    print("Map not found\nGenerating new map ...")
    file = open("map_save.json","w")
    file.write(json.dumps(carte.map, indent = 4))
    file.close()
print("Carte 100%")

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_running = True
server_restart = False
clients_connectes = []
#infos_connectes = []

thread_filler = Filler(carte)
thread_filler.start()
thread_filler.on = False

#thread_check_connection = Check_Connection_Server(clients_connectes)
#thread_check_connection.start()
#thread_filler.on = False


while serveur_running:
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        clients_connectes.append(connexion_avec_client)
        #infos_connectes.append(infos_connexion)

    #thread_check_connection.replace_client_liste(clients_connectes)
    #for client in thread_check_connection.client_to_remove:
    #    try:
    #        clients_connectes.remove(client)
    #        client.close()
    #        thread_check_connection.client_to_remove.remove(client)
    #    except:
    #        pass


    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
        for client in clients_a_lire:
            msg_recu = ""
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()

            if "/" in msg_recu:

                if msg_recu == "/ping":
                    print("Called command ping")
                    client.send(b"pong")

                elif msg_recu == "/help":
                    print("Called command help")
                    client.send(b"Liste des commandes : help / stop / ping / show / dig (x_arg) (y_arg) / fill (x_arg) (y_arg) / broadcast (arg) / display / dig_all / fill_all / t_start / t_stop / disconnect")          

                elif msg_recu == "/stop":
                    print("Called command stop")
                    client.send(b"Closing server ...")
                    carte.save_to_json("map_save.json")
                    serveur_running = False
                    print("Closing server ...")

                elif msg_recu == "/restart":
                    print("Called command restart")
                    client.send(b"Restarting server ...")
                    carte.save_to_json("map_save.json")
                    serveur_running = False
                    server_restart = True
                    print("Restarting server ...")

                elif msg_recu == "/disconnect":
                    print("Disconnect client : ...")
                    client.send(b"Disconnection ...")
                    clients_connectes.remove(client)
                    client.close()
                    #thread_check_connection.replace_client_liste(clients_connectes)

                elif "/broadcast" in msg_recu :
                    print("Called command broadcast")
                    arg = extract_argument(msg_recu)
                    broadcast(clients_connectes,msg_recu.encode())

                elif msg_recu == "/t_start":
                    print("Called command tstart")
                    thread_filler.on = True
                    client.send(b"Thread Started")

                elif msg_recu == "/t_stop":
                    print("Called command tstop")
                    thread_filler.on = False
                    client.send(b"Thread Stoped")

                elif msg_recu == "/show":
                    print("Called command show")
                    client.send(json.dumps(carte.map, indent = 4).encode())

                elif msg_recu == "/display":
                    print("Called command display")
                    client.send(carte.display().encode())

                elif "/dig" in msg_recu:
                    arg = extract_argument(msg_recu)
                    if arg[1] == "all":
                        print("Called command dig_all")
                        carte.dig_all()
                        client.send(b"Dig All complete")
                    else:
                        print("Called command dig i j")
                        carte.dig(int(arg[1]),int(arg[2]))
                        client.send(b"Dig complete")

                elif "/fill" in msg_recu:
                    arg = extract_argument(msg_recu)
                    if arg[1] == "all":
                        print("Called command fill_all")
                        carte.fill_all()
                        client.send(b"Fill All complete")
                    else:
                        print("Called command fill i j")
                        carte.fill(int(arg[1]),int(arg[2]))
                        client.send(b"Fill complete")

                else:
                    print("Unknowned command")
                    client.send(b"Unknowned command")

            else: 
                if msg_recu == "Ping_Return":
                    #thread_check_connection.i = 6
                    print("Ping_Returned")

                elif msg_recu == "get_map_update":
                    client.send(carte.map_to_string().encode())

    except select.error:
        pass


print("Closing connection")
thread_filler.on = False
thread_filler.kill = False
#thread_check_connection.on = False
#thread_check_connection.kill = False
for client in clients_connectes:
    client.close()

connexion_principale.close()

if server_restart:
    os.system('python server.py')