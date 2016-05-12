from tkinter import *
#import Objects.py
#import Creation.py


graph = []
indice = 0
tour = []

def maj(graph):
    """Mets à jour le tkinter"""

    canvas.delete("all")
    graph.drawGraph()
    connex.config(text = "Connexité : " + str(graph.isConnex()), fg = "green" if graph.isConnex() else "red")
    eulerien.config(text = "Eulerien : " + str(graph.existeTour()), fg = "green" if graph.existeTour() else "red")
    action.grid_remove()

def generate():
    """Génère un nouveau graphe aléatoire et l'affiche"""
    global graph
    
    n = int(entryVertices.get())
    p = float(entryProba.get())
    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            graph.addEdge(i, j)
    maj(graph)
    nextEdgeEuler.grid_remove()
    drawEulerTour.grid(row = 3, column = 5, columnspan = 6)
    


def makeEuler():
    """Modifie un graphe pour le rendre Eulerien"""
    global graph

    makeEulerian(graph)
    maj(graph)


def drawEuler():
    """Affiche un tour eulerien"""
    global graph, itera, tour

    tour = graph.findEulerianTour()
    drawEulerTour.grid_remove()
    nextEdgeEuler.grid(row = 3, column = 5, columnspan = 2)
    itera = nextEuler(tour)


def nextEuler(tour):
    """Affiche le prochain edge du tour d'Euler"""
    global graph

    for i in range(len(tour)-1):
        if tour[i] < tour[i+1]:
            canvas.itemconfig(edges[str(tour[i])+" "+str(tour[i+1])], fill = "green")
        else:
            canvas.itemconfig(edges[str(tour[i+1])+" "+str(tour[i])], fill = "green")
        yield


def nextEulerEnd():
    global graph, itera

    try:
        next(itera)
    except StopIteration:
        nextEdgeEuler.grid_remove()
        drawEulerTour.grid(row = 3, column = 5, columnspan = 2)

