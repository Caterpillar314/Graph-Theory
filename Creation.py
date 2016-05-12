#from Objects.py import *
from random import random
from math import e, pi


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

    # Gere les vertices de degre n-1
    complet = [vertex for vertex in graph.listeSommets if vertex.getDegre() == graph.taille-1]
    for vertex in complet:
        # Choisis en priorité les voisins de degré impair
        index = sorted(vertex.adjacence, key = lambda v:graph.listeSommets[v].getDegre()%2 == 0)[0]
        indVoisin = vertex.adjacence.index(index)
        vertex.adjacence.pop(indVoisin)
        vertex.edges.pop(indVoisin)
        indVertex = graph.listeSommets[index].adjacence.index(vertex.id)
        graph.listeSommets[index].adjacence.pop(indVertex)
        graph.listeSommets[index].edges.pop(indVertex)

    # Gere les vertices de degre impair
    wrongVertices = [vertex for vertex in graph.listeSommets if vertex.getDegre()%2 == 1 or vertex.getDegre() == 0]
    wrongVertices.sort(key = lambda vertex:len([1 for v in vertex.adjacence if v in wrongVertices]))
    while wrongVertices != []:
        vertex = wrongVertices.pop(0)
        # Filtre les vertices possibles pour faire un lien avec le vertex actuel
        choix = list(filter(lambda v:v.id not in vertex.adjacence, wrongVertices))
        
        # Si on peut faire un lien avec un vertex de degré impair ou de degré nul:
        if choix != []:
            voisin = choix[0]
            graph.addEdge(vertex.id, voisin.id, True)
            if voisin.getDegre() != 1:
                wrongVertices.remove(voisin)
        else:
            # Si aucun vertex ne peut être lié avec le vertex actuel, on en choisit un de degré pair
            # que l'on rajoute dans la liste des vertices de degré impair
            choix = list(filter(lambda v:v.id not in vertex.adjacence and v.id != vertex.id and v.getDegre() < graph.taille-3, graph.listeSommets))
            
            # Si vraiment aucun vertex ne peut être lié, alors on enlève un vertex, en priorité sur les voisins de degré impair
            if choix == []:
                index = sorted(vertex.adjacence, key = lambda v:graph.listeSommets[v].getDegre()%2 == 0)[0]
                indVoisin = vertex.adjacence.index(index)
                vertex.adjacence.pop(indVoisin)
                vertex.edges.pop(indVoisin)
                indVertex = graph.listeSommets[index].adjacence.index(vertex.id)
                graph.listeSommets[index].adjacence.pop(indVertex)
                graph.listeSommets[index].edges.pop(indVertex)
                
                # Si le voisin avait un degré impair, il a maintenant un degré pair:
                # on l'enlève donc de la liste wrongVertices
                if graph.listeSommets[index].getDegre()%2 == 0:
                        wrongVertices.remove(graph.listeSommets[index])

            else:
                voisin = choix[0]
                wrongVertices.append(voisin)
                graph.addEdge(vertex.id, voisin.id, True)
	
        if vertex.getDegre() == 1:
            wrongVertices.append(vertex)

