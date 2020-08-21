"""Module map"""
import json
import sys
import random
from threading import Thread
import time

def extract_dim_from_string(arg):
    liste1 = [i for i in arg]
    j = 0
    lettre = ""
    writting = False
    for i in liste1:
        if i == ")":
            writting = False
        if writting:
            lettre += liste1[j]
        j += 1
        if i == "(":
            writting = True
    lettre = lettre.replace(",",' ')
    lettre = lettre.replace("/",' ')
    liste2 = lettre.split()
    if len(liste2) != 2:
        return [[0],[0]]
    else:
        return liste2

def extract_argument(arg):
    liste = arg.split()
    return liste 

def broadcast(client_list,data):
    for i in range(len(client_list)):
        print(data)
        client_list[i].send(data)

class Carte:
    def __init__(self,dimX,dimY):
        self.dimX = dimX
        self.dimY = dimY
        self.minX = 0
        self.maxX = dimX
        self.minY = 0
        self.maxY = dimY
        self.default = "Ungenerated"
        self.map = {}
        for i in range(dimX):
            for j in range(dimY):
                self.map[str(i)+"/"+str(j)] = self.default   

    def display(self):
        string_to_return = ""
        j = 0
        for i in self.map:
            string_to_return += self.map[i].center(20)
            j += 1
            if j == self.dimX:
                string_to_return += "\n\n"
                j = 0  
        return(string_to_return)

    def map_to_string(self):
        string_to_return = ""
        string_to_return += str(self.dimX) + " "
        string_to_return += str(self.dimY) + " "
        for i in self.map:
            string_to_return += str(self.map[i]) + " "
        return(string_to_return)

    def string_to_map(self, string):
        x = 0
        liste = string.split()
        self.dimX = int(liste[0])
        self.dimY = int(liste[1])
        liste.remove(str(self.dimX))
        liste.remove(str(self.dimY))
        for i in range(self.dimX):
            for j in range(self.dimY):
                self.map[str(i)+"/"+str(j)] = liste[x]
                x += 1
        

    def empty(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                self.map[str(i)+"/"+str(j)] = "Void"

    def dig_all(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                self.map[str(i)+"/"+str(j)] = "Void"

    def dig(self,x,y):
        if x >= self.dimX or y >= self.dimY:
            print("Out of bound Map")
        else:
            self.map[str(x)+"/"+str(y)] = "Void"

    def fill_all(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                self.map[str(i)+"/"+str(j)] = "Grass"

    def fill(self,x,y):
        if x >= self.dimX or y >= self.dimY:
            print("Out of bound Map")
        else:
            self.map[str(x)+"/"+str(y)] = "Grass"

    def load_from_json(self,url):
        file = open(url,"r")
        contenu = file.read()
        self.map = json.loads(contenu)
        file.close()

    def save_to_json(self,url):
        file = open(url,"w")
        file.write(json.dumps(self.map, indent = 4))
        file.close()

    def determine_dimensions(self):
        lettre = ""
        liste = []
        for i in self.map:
            lettre = i.replace("/",' ')
            liste = lettre.split()
            liste = [int(i) for i in liste]
            if liste[0] < self.minX:
                self.minX = liste[0]
            if liste[0] > self.maxX:
                self.maxX = liste[0]
            if liste[1] < self.minY:
                self.minY = liste[1]
            if liste[1] > self.maxY:
                self.maxY = liste[1]
        self.dimX = self.maxX - self.minX
        self.dimY = self.maxY - self.minY


class Filler(Thread):
    def __init__(self, carte):
        Thread.__init__(self)
        self.on = False
        self.kill = True
        self.carte = carte

    def run(self):
        self.on = True
        while self.kill:
            if self.on:
                sys.stdout.write("Filled | ")
                sys.stdout.flush()
                attente = 2
                time.sleep(attente)
                self.carte.fill(random.randrange(0,self.carte.dimX,1),random.randrange(0,self.carte.dimY,1))

class Check_Connection_Server(Thread):
    def __init__(self, client_liste):
        Thread.__init__(self)
        self.client_liste = client_liste
        self.on = False
        self.kill = True
        self.i = 6
        self.client_to_remove = []

    def run(self):
        self.on = True
        while self.kill:
            if self.on:
                for client in self.client_liste:
                    time.sleep(5)
                    self.i -= 1
                    if self.i <= 0:
                        print("Il est deco pour de bon")
                        try:
                            self.client_to_remove.append(client)
                        except:
                            pass
                    else:
                        print("Ping send to client")
                        try:
                            client.send(b"Ping_Send")
                        except:
                            print("Il est deco ? i = " + str(self.i))

    def replace_client_liste(self,client_list):
        self.client_liste = client_list


class Check_Connection_Client(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection
        self.on = False
        self.kill = True

    def run(self):
        self.on = True
        while self.kill:
            if self.on:
                time.sleep(5)
                data = self.connection.recv(1024)
                data = data.decode()
                if data == "Ping_Send":
                    self.connection.send(b"Ping_Return")


class Check_Connection_Client(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection
        self.on = False
        self.kill = True

    def run(self):
        self.on = True
        while self.kill:
            if self.on:
                time.sleep(5)
                data = self.connection.recv(1024)
                data = data.decode()
                if data == "Ping_Send":
                    self.connection.send(b"Ping_Return")


# test du module
#if __name__ == "__main__":
    #extract_argument("broad salut")