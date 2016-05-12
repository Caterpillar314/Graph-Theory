from random import random
from math import e, pi


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
        
        self.debug = []
                
    def __str__(self):
        return "Je suis un graphe à " + str(self.taille) + " sommets."
        
    def addVertex(self, n = 1):
        """Ajoute n vertices au graph"""
        for i in range(n):
            self.listeSommets.append(Vertex(i))
        self.taille += n

    def drawGraph(self):
        global edges
        
        for v in self.listeSommets :
            v.getCoord(self.taille)
            canvas.create_oval(v.coordX-5, v.coordY-5, v.coordX+5, v.coordY+5, fill = "blue")
            z = (haut/2-35)*e**(pi*2j*v.id/self.taille)
            x, y = larg/2+z.real, haut/2+z.imag
            canvas.create_text(x, y, text = str(v))

        edges = dict()
        for v in self.listeSommets:
            for idNumb in v.adjacence:
                if idNumb > v.id:
                    edges[str(v.id)+" "+str(idNumb)] = canvas.create_line(v.coordX, v.coordY, self.listeSommets[idNumb].coordX, self.listeSommets[idNumb].coordY, fill = "red")
        canvas.pack()

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
        """Retourne un cycle dans le graphe a partir du vertex #debut"""
        
        for v in self.listeSommets:
            v.chemin = []
            
        checked = set()
        liste = [self.listeSommets[debut]]
        for n in range(self.taille+5):
            vertex = liste.pop(0)
            checked.add(vertex.id)
            for w in vertex.adjacence:
                if w not in checked and vertex.edges[vertex.adjacence.index(w)] and \
                (len(vertex.chemin) <= 1 or len(self.listeSommets[w].chemin) <= 1 or self.listeSommets[w].chemin[1] != vertex.chemin[1]):
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
            return [vertex]

        # Récurrence :
        # On trouve un cycle
        cycle = self.findCycle(vertex)

        # On met à jour les vertex utilisés dans le cycle :
        for i in range(len(cycle)-1):
            v = self.listeSommets[cycle[i]]
            index =  v.adjacence.index(cycle[i+1])                  # Index d'apparition du vertex \cycle[i+1]\ dans la table d'adjacence
            v.edges[index] = False
            self.debug.append((v.id, index))
            v = self.listeSommets[cycle[i+1]]
            index = v.adjacence.index(cycle[i])
            v.edges[index] = False            

        # Pour chaque sommets de ce cycle, on va trouver un nouveau cycle
        tour = []
        for i in range(0, len(cycle)):
            tour.extend(self.findEulerianTourAux(cycle[i]))

        return tour
        
            
