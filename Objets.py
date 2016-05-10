#from pylab import *
from random import random
from math import e, pi
from tkinter import *


###############################################################################################################
# Tkinter (module préinstallé en python assez simple d'utilisation)
haut, larg = 900, 900

fenetre = Tk()
canvas = Canvas(fenetre, width = larg, height = haut, bg = "white")
canvas.grid()


###############################################################################################################
# Classes principales

class Vertex():
    
    def __init__(self, idNumb):
        self.id = idNumb
        self.coordX = 0
        self.coordY = 0
        self.adjacence = []
        self.chemin = []
        
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
        #return "Je suis le sommet {0}, situé aux coordonnées ({1}, {2})".format(str(self.id), str(self.coordX), str(self.coordY))
        
    def getCoord(self, tailleGraph):
        """Mets à jour les coordonnés du vertex en vu de l'affichage"""
        z = (haut/2-50)*e**(pi*2j*self.id/tailleGraph)
        self.coordX = larg/2+z.real
        self.coordY = haut/2+z.imag

    def getDegre(self):
        """Retourne le degré du vertex"""
        return len(self.adjacence)



class Graph():
    
    def __init__(self, probaEdge):
        self.taille = 0
        self.listeSommets = []
        self.probaEdge = probaEdge
                
    def __str__(self):
        return "Je suis un graphe à " + str(self.taille) + " sommets."
        
    def addVertex(self, n = 1):
        """Ajoute n vertices au graph"""
        for i in range(n):
            self.listeSommets.append(Vertex(i))
        self.taille += n

    def drawGraph(self):
        for v in self.listeSommets :
            v.getCoord(self.taille)
            #plot([v.coordX], [v.coordY], 'o-')
            canvas.create_oval(v.coordX-5, v.coordY-5, v.coordX+5, v.coordY+5, fill = "blue")
            canvas.create_text(v.coordX+10, v.coordY+10, text = str(v))
            
        for v in self.listeSommets:
            for idNumb in v.adjacence:
                canvas.create_line(v.coordX, v.coordY, self.listeSommets[idNumb].coordX, self.listeSommets[idNumb].coordY, fill = "red")

    def addEdge(self, i, j):
        """Ajoute un edge entre les sommets i et j avec la probabilité probaEdge"""
        if random() < self.probaEdge:
            self.listeSommets[i].adjacence.append(j)
            self.listeSommets[j].adjacence.append(i)

    def isConnex(self):
        """Retourne si le graphe est connexe ou non"""
        
        if not all([vertex.getDegre() != 0 for vertex in self.listeSommets]):
            return False
        
        checked = set()
        liste = [self.listeSommets[0]]
        while len(liste) != 0 and len(checked) < self.taille:
            vertex = liste.pop(0)
            checked.add(vertex.id)
            for v in vertex.adjacence:
                if v not in checked and self.listeSommets[v] not in liste:
                    liste.append(self.listeSommets[v])
        return self.taille == len(checked)

    def existeTour(self):
        """Retourne s'il existe un tour d'Euler dans le graphe"""
        return self.isConnex() and all([vertex.getDegre()%2 == 0 for vertex in self.listeSommets])


    def findCycle(self):
        """Retourne un cycle dans le graphe"""
        for v in self.listeSommets:
            v.chemin = []
            
        checked = set()
        liste = [self.listeSommets[0]]
        for n in range(self.taille+5):
            vertex = liste.pop(0)
            checked.add(vertex.id)
            for w in vertex.adjacence:
                if w not in checked:
                    v = self.listeSommets[w]
                    if v.chemin != []:
                        return v.chemin + [v.id, vertex.id] + vertex.chemin[::-1]
                    else:
                        v.chemin = vertex.chemin + [vertex.id]
                    liste.append(v)



###############################################################################################################
# Main

def createGraph(n = 100, p = 0.5):
    """Retourne un graphe aléatoire de n vertex avec une probabilité d'edge p"""

    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            graph.addEdge(i, j)
    return graph




def affiche(graph):
    """Affiche un graphe"""
    canvas.delete("all")
    graph.drawGraph()
