# -*- coding: cp1252 -*-
from random import random, randrange, choice
from math import e, pi
#from tkinter import *


###############################################################################################################
# Tkinter
haut, larg = 900, 900

#fenetre = Tk()
#canvas = Canvas(fenetre, width = larg, height = haut, bg = "white")
#canvas.grid()


###############################################################################################################
# Classes principales

class Vertex():
    
    def __init__(self, idNumb):
        self.id = idNumb
        self.coordX = 0
        self.coordY = 0
        self.adjacence = []
        self.edges = []
        self.chemin = []
        
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
        #return "Je suis le sommet {0}, situé aux coordonnées ({1}, {2})".format(str(self.id), str(self.coordX), str(self.coordY))

    def __int__(self):
        return int(self.id)
        
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

    def addEdge(self, i, j, sure = False):
        """Ajoute un edge entre les sommets i et j avec la probabilité probaEdge"""
        if random() < self.probaEdge or sure:
            self.listeSommets[i].adjacence.append(j)
            self.listeSommets[i].edges.append(True)
            self.listeSommets[j].adjacence.append(i)
            self.listeSommets[j].edges.append(True)

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


    def findCycle(self, debut = 0):
        """Retourne un cycle dans le graphe"""        
        for v in self.listeSommets:
            v.chemin = []
            
        checked = set()
        liste = [self.listeSommets[debut]]
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

    def findEulerianTour(self):

        if not self.existeTour():
            return "Il n'y a pas de tour d'Euler possible dans ce graphe"

        else:
            return self.findEulerianTourAux(0)

    def findEulerianTourAux(self, vertex):
        """Retourne un tour d'Euler dans le graphe"""

        # Cas initial :
        # si tous les edges partant de vertex ont déjà été utilisés dans le tour, on retourne rien
        if True not in self.listeSommets[vertex].edges:
            print("Une feuille !")
            print(vertex)
            print(self.listeSommets[vertex].edges)
            return [vertex]

        # Récurrence :
        # On trouve un cycle
        cycle = self.findCycle(vertex)
        print("Vertex :", vertex)
        print("Cycle : ", cycle)
        print()

        # On met à jour les vertex utilisés dans le cycle :
        for i in range(len(cycle)-1):
            v = self.listeSommets[cycle[i]]
            print("Voisin : ", v)
            index =  v.adjacence.index(cycle[i+1])                  # Index d'apparition du vertex \cycle[i+1]\ dans la table d'adjacence
            v.edges[index] = False
            print("Voisin.edge apres maj : ", v.edges)
            

        # Pour chaque sommets de ce cycle, on va trouver un nouveau cycle
        tour = []
        for i in range(len(cycle)-1):
            tour.append(self.findEulerianTourAux(cycle[i]))

        return tour
        
            



###############################################################################################################
# Main

def createGraph(n = 50, p = 0.25):
    """Retourne un graphe aléatoire de n vertex avec une probabilité d'edge p"""

    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            graph.addEdge(i, j)
    return graph


def makeEulerian(graph):
    """Ajoute des edges à un graphe jusqu'à ce que celui ci contienne un tour d'Euler"""

    wrongVertices = [vertex for vertex in graph.listeSommets if vertex.getDegre()%2 == 1 or vertex.getDegre() == 0]
    while wrongVertices != []:
        vertex = wrongVertices.pop(0)
        choix = list(filter(lambda v:v.id not in vertex.adjacence, wrongVertices))
        if choix != []:
            voisin = choice(choix)
        else:
            voisin = choice(list(filter(lambda v:v.id not in vertex.adjacence and v.id != vertex.id, graph.listeSommets)))
            wrongVertices.append(voisin)
        graph.addEdge(vertex.id, voisin.id, True)
        if voisin.getDegre() != 1 and choix != []:
            wrongVertices.remove(voisin)
        if vertex.getDegre() == 1:
            wrongVertices.append(vertex)


def affiche(graph):
    """Affiche un graphe"""
    canvas.delete("all")
    graph.drawGraph()


g = createGraph(50, 0.5)
print(sum([v.getDegre() for v in g.listeSommets]))
print("The graph is connex : ", g.isConnex())
print("The graph has an Eulerian tour : ", g.existeTour())
makeEulerian(g)
print("After modification , the graph has an Eulerian tour : ", g.existeTour())
for v in g.listeSommets:
    print str(v) + " : " + ", ".join(map(str, v.adjacence))
print(g.findEulerianTour())
