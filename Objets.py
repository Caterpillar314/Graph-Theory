from pylab import *

class Vertex():
    def __init__(self, id):
        self.id = id
        self.coordX = 0
        self.coordY = 0
        self.degre = 0
        
    def __str__(self):
        return("Je suis le sommet"+str(self.id)+", situé aux coordonnées : "+str(self.coordX)+", "+str(self.coordY))
        
    
    def getCoord(self, tailleGraph):
        z = e**(pi*2j*self.id/tailleGraph)
        self.coordX = z.real
        self.coordY = z.imag



class Graph():
    def __init__(self, probaEdge):
        self.taille = 0
        self.listeSommets = []
        self.listeAdjacence = []
        self.probaEdge = probaEdge
                
    def __str__(self):
        return("Je suis un graphe à "+str(self.taille)+" sommets.")
        

    def addVertex(self):
        (self.listeSommets).append(Vertex(self.taille + 1))
        self.taille += 1


    def drawGraph(self):
        #pour l'instant, seuls les sommets sont représentés
        for v in self.listeSommets :
            v.getCoord(self.taille)
            plot([v.coordX], [v.coordY], 'o-')
        xlim([-1.5, 1.5])
        ylim([-1.5, 1.5])
        show()


    def addEdge(self, i, j):
        """ajoute un edge entre les sommets i et j avec la probabilité probaEdge"""
        #modif liste adjacence + degre des sommets
        pass

    
    def existeTour(self):
        pass