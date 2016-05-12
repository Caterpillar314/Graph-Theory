#import GUI.py
from tkinter import *



haut, larg = 650, 900

edges = dict()
fenetre = Tk()


canvas = Canvas(fenetre, width = larg, height = haut, bg = "white")
canvas.grid(row = 2, column = 1, rowspan = 2, columnspan = 4)

connex = Label(fenetre, text = "Connexité")
connex.grid(row = 4, column = 3)

eulerien = Label(fenetre, text = "Eulerien")
eulerien.grid(row = 4, column = 2)

vertices = Label(fenetre, text = "Number of vertices")
vertices.grid(row = 1, column = 1, sticky = E)

proba = Label(fenetre, text = "Probability for edges")
proba.grid(row = 1, column = 3, sticky = E)

entryVertices = Entry(fenetre)
entryVertices.grid(row = 1, column = 2)

entryProba = Entry(fenetre)
entryProba.grid(row = 1, column = 4)

action = Label(fenetre, text = "Enter a number of vertices\nand a probability", bg = "red")
action.grid(row = 2, column = 4)

new_graph = Button(fenetre, text = "Generate a new graph", command = generate)
new_graph.grid(row = 2, column = 5)

make_euler = Button(fenetre, text = "Make the graph Eulerian", command = makeEuler)
make_euler.grid(row = 2, column = 6)

drawEulerTour = Button(fenetre, text = "Draw an Eulerian tour", command = drawEuler)
drawEulerTour.grid(row = 3, column = 5, columnspan = 2)

nextEdgeEuler = Button(fenetre, text = "Next", command = nextEulerEnd)

fenetre.mainloop()